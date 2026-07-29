// The whole agent runtime: one stateless drafting run.
// Ticket in → tool loop (read-only) → validated JSON draft out.
// The caller (filteronme-one's webhook handler) persists the result; this
// process writes nothing and cannot send email.

import { generateText, stepCountIs } from "ai";
import { z } from "zod";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { makeTools } from "./tools/lookups.ts";
import type { RunContext } from "./tools/shared.ts";

const MODEL = process.env.AGENT_MODEL ?? "anthropic/claude-sonnet-5";

export const TicketPayload = z.object({
  ticketRef: z.string().min(1),
  subject: z.string().default(""),
  customerEmail: z.string().email(),
  messages: z
    .array(
      z.object({
        direction: z.enum(["inbound", "outbound", "note"]),
        author: z.string().default(""),
        bodyText: z.string(),
        createdAt: z.string().default(""),
      }),
    )
    .min(1),
});
export type TicketPayload = z.infer<typeof TicketPayload>;

export const DraftResult = z.object({
  topic: z.string(),
  action: z.enum(["draft", "no-reply", "escalate"]),
  needs_human: z.boolean(),
  draft: z.string(),
  lookups_needed: z.array(z.string()).default([]),
  rationale: z.string(),
});
export type DraftResult = z.infer<typeof DraftResult>;

function loadBrain(): string {
  const root = process.cwd();
  const instructions = readFileSync(join(root, "agent/instructions.md"), "utf8");
  const index = readFileSync(join(root, "playbooks/README.md"), "utf8");
  const tone = readFileSync(join(root, "playbooks/TONE.md"), "utf8");
  return [
    instructions,
    "\n---\n# Playbook index (call read_playbook for the matched topic)\n",
    index,
    "\n---\n# Tone rules\n",
    tone,
  ].join("\n");
}

function renderTicket(ticket: TicketPayload): string {
  const lines = [
    `Ticket ${ticket.ticketRef}`,
    `From: ${ticket.customerEmail}`,
    `Subject: ${ticket.subject || "(no subject)"}`,
    "",
  ];
  for (const m of ticket.messages) {
    lines.push(
      `--- ${m.direction}${m.author ? ` (${m.author})` : ""} ${m.createdAt} ---`,
      m.bodyText.trim(),
      "",
    );
  }
  return lines.join("\n");
}

function collectAllowedEmails(ticket: TicketPayload): Set<string> {
  const found = new Set<string>([ticket.customerEmail.toLowerCase()]);
  const re = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
  for (const m of ticket.messages) {
    for (const hit of m.bodyText.match(re) ?? []) found.add(hit.toLowerCase());
  }
  return found;
}

function extractJson(text: string): unknown {
  // The final assistant text should end with a JSON object; be tolerant of
  // stray prose or fences before it.
  const start = text.lastIndexOf("{\n");
  const candidates = [text, text.slice(start >= 0 ? start : 0)];
  for (const candidate of candidates.reverse()) {
    const match = candidate.match(/\{[\s\S]*\}/);
    if (!match) continue;
    try {
      return JSON.parse(match[0]);
    } catch {
      continue;
    }
  }
  throw new Error("no JSON object in model output");
}

export async function runDraftAgent(input: unknown): Promise<DraftResult> {
  const ticket = TicketPayload.parse(input);
  const ctx: RunContext = {
    ticketRef: ticket.ticketRef,
    allowedEmails: collectAllowedEmails(ticket),
  };
  const system = loadBrain();
  const tools = makeTools(ctx);

  let lastError = "";
  for (let attempt = 0; attempt < 2; attempt++) {
    const result = await generateText({
      model: MODEL,
      system,
      prompt:
        renderTicket(ticket) +
        (lastError
          ? `\n\n(Previous output was invalid: ${lastError}. Reply with ONLY the JSON object.)`
          : ""),
      tools,
      stopWhen: stepCountIs(10),
    });
    try {
      const parsed = DraftResult.parse(extractJson(result.text));
      // Belt-and-suspenders (rule 2b): drafts that promise action escalate.
      if (/\bI(?:'| wi)ll (check|look into|follow up|get back)/i.test(parsed.draft)) {
        parsed.action = "escalate";
        parsed.needs_human = true;
      }
      console.log(
        JSON.stringify({
          t: "agent_run",
          ticketRef: ticket.ticketRef,
          topic: parsed.topic,
          action: parsed.action,
          needs_human: parsed.needs_human,
          usage: result.usage,
        }),
      );
      return parsed;
    } catch (err) {
      lastError = err instanceof Error ? err.message : "invalid output";
    }
  }
  // Guardrail 4: failure to produce valid output = escalation, never a guess.
  return {
    topic: "other",
    action: "escalate",
    needs_human: true,
    draft: "",
    lookups_needed: [],
    rationale: `Agent could not produce a valid draft (${lastError}); escalating.`,
  };
}
