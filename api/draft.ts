// POST /api/draft — the agent's only entry point.
// Called by filteronme-one's inbound-email webhook handler with a ticket
// payload; returns the DraftResult JSON. Auth: shared internal secret.

import { timingSafeEqual } from "node:crypto";
import { runDraftAgent } from "../agent/run.ts";

export const maxDuration = 300;

function authorized(request: Request): boolean {
  const secret = process.env.INTERNAL_WEBHOOK_SECRET ?? "";
  const given = request.headers.get("x-internal-secret") ?? "";
  if (!secret || given.length !== secret.length) return false;
  return timingSafeEqual(Buffer.from(given), Buffer.from(secret));
}

export async function POST(request: Request): Promise<Response> {
  if (!authorized(request)) {
    return Response.json({ error: "unauthorized" }, { status: 401 });
  }
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "invalid JSON body" }, { status: 400 });
  }
  try {
    const result = await runDraftAgent(body);
    return Response.json(result);
  } catch (err) {
    const message = err instanceof Error ? err.message : "agent run failed";
    console.log(JSON.stringify({ t: "agent_error", message }));
    // Portal treats a 500 as "no draft; show ticket as needs-human".
    return Response.json({ error: message }, { status: 500 });
  }
}
