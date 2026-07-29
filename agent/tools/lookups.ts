// The D20 tool whitelist. One fixed query per tool, read-only, guarded.
// Shape kept eve-compatible (zod inputSchema + execute) so a future eve
// migration is file moves, not rewrites.

import { tool } from "ai";
import { z } from "zod";
import type { RunContext } from "./shared.ts";
import {
  assertAllowedEmail,
  censorEmail,
  instrumented,
  queryRows,
  stripeGet,
} from "./shared.ts";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const PLAYBOOKS_DIR = join(process.cwd(), "playbooks");

export function makeTools(ctx: RunContext) {
  return {
    read_playbook: tool({
      description:
        "Read one topic playbook in full. Call this for the matched topic " +
        "BEFORE drafting. Valid slugs are listed in the playbook index.",
      inputSchema: z.object({ slug: z.string().regex(/^[a-z][a-z0-9-]{2,40}$/) }),
      execute: instrumented(ctx, "read_playbook", async ({ slug }: { slug: string }) => {
        const NOT_TOPICS = new Set(["README", "TONE", "OPEN-QUESTIONS"]);
        const valid = readdirSync(PLAYBOOKS_DIR)
          .filter((f) => f.endsWith(".md"))
          .map((f) => f.replace(/\.md$/, ""))
          .filter((slug) => !NOT_TOPICS.has(slug));
        if (!valid.includes(slug)) {
          return { error: `Unknown playbook "${slug}". Valid: ${valid.join(", ")}` };
        }
        return { slug, content: readFileSync(join(PLAYBOOKS_DIR, `${slug}.md`), "utf8") };
      }),
    }),

    get_account_by_email: tool({
      description:
        "Look up a FilterOnMe app account by email (read-only). Returns " +
        "premium status, free-premium grant, and trial timing.",
      inputSchema: z.object({ email: z.string().email() }),
      execute: instrumented(ctx, "get_account_by_email", async ({ email }: { email: string }) => {
        const addr = assertAllowedEmail(ctx, email);
        const users = await queryRows(
          "SELECT `isPremium`, `subscriptionId` IS NOT NULL AS hasSubscription, " +
            "`trialStartedAt`, `createdAt` FROM `User` WHERE LOWER(email) = ? LIMIT 1",
          [addr],
        );
        const freePremium = await queryRows(
          "SELECT expires FROM `FreePremium` " +
            "WHERE LOWER(email) = ? AND (expires IS NULL OR expires > NOW()) LIMIT 1",
          [addr],
        );
        if (users.length === 0 && freePremium.length === 0) {
          return { exists: false };
        }
        const u = users[0];
        const trialStartedAt: Date | null = u?.trialStartedAt ?? null;
        const RESET_MS = 42 * 24 * 3600 * 1000; // 6 weeks, code-verified fact
        return {
          exists: true,
          isPremium: Boolean(u?.isPremium),
          hasStripeSubscription: Boolean(u?.hasSubscription),
          hasFreePremiumGrant: freePremium.length > 0,
          accountCreatedAt: u?.createdAt ?? null,
          trialStartedAt,
          trialResetEligibleAt: trialStartedAt
            ? new Date(trialStartedAt.getTime() + RESET_MS)
            : null,
        };
      }),
    }),

    get_subscription_by_email: tool({
      description:
        "Look up the Stripe subscription for an email (read-only). Use to " +
        "verify subscription state before referencing it in a draft, and for " +
        "the verified-owner cancellation check.",
      inputSchema: z.object({ email: z.string().email() }),
      execute: instrumented(ctx, "get_subscription_by_email", async ({ email }: { email: string }) => {
        const addr = assertAllowedEmail(ctx, email);
        const customers = await stripeGet("/customers", { email: addr, limit: "3" });
        for (const customer of customers.data ?? []) {
          const subs = await stripeGet("/subscriptions", {
            customer: customer.id,
            status: "all",
            limit: "3",
          });
          const sub = (subs.data ?? []).sort(
            (a: any, b: any) => b.created - a.created,
          )[0];
          if (!sub) continue;
          const subEmail = (customer.email ?? "").toLowerCase();
          return {
            found: true,
            status: sub.status,
            plan: sub.items?.data?.[0]?.plan?.interval ?? "unknown",
            cancelAtPeriodEnd: sub.cancel_at_period_end === true,
            currentPeriodEnd: new Date(sub.current_period_end * 1000).toISOString(),
            // full address only when it IS the address that was asked about;
            // otherwise censored so drafts can't leak it
            subscriptionEmail: subEmail === addr ? subEmail : censorEmail(subEmail),
            emailMatchesTicket: subEmail === addr && ctx.allowedEmails.has(subEmail),
          };
        }
        return { found: false };
      }),
    }),

    get_recent_charges: tool({
      description:
        "Last few Stripe charges for an email (read-only). Use for " +
        "charged-after-cancel, duplicate-charge, and refund-context checks.",
      inputSchema: z.object({
        email: z.string().email(),
        limit: z.number().int().min(1).max(5).default(3),
      }),
      execute: instrumented(ctx, "get_recent_charges", async ({ email, limit }: { email: string; limit: number }) => {
        const addr = assertAllowedEmail(ctx, email);
        const customers = await stripeGet("/customers", { email: addr, limit: "3" });
        const charges: object[] = [];
        for (const customer of customers.data ?? []) {
          const page = await stripeGet("/charges", {
            customer: customer.id,
            limit: String(limit),
          });
          for (const ch of page.data ?? []) {
            charges.push({
              date: new Date(ch.created * 1000).toISOString().slice(0, 10),
              amountUsd: ch.amount / 100,
              status: ch.status,
              refunded: ch.refunded === true,
              disputed: ch.disputed === true,
            });
          }
        }
        return { charges: charges.slice(0, limit) };
      }),
    }),

    get_ticket_history: tool({
      description:
        "Previous support tickets from this customer in the portal " +
        "(read-only). Use to avoid repeating advice that already failed.",
      inputSchema: z.object({ email: z.string().email() }),
      execute: instrumented(ctx, "get_ticket_history", async ({ email }: { email: string }) => {
        const addr = assertAllowedEmail(ctx, email);
        try {
          const tickets = await queryRows(
            "SELECT id, subject, topic, status, `createdAt` FROM `SupportTicket` " +
              "WHERE LOWER(`customerEmail`) = ? ORDER BY `createdAt` DESC LIMIT 5",
            [addr],
          );
          return { tickets };
        } catch {
          // Support tables may not exist until the portal migration lands.
          return { tickets: [], note: "ticket history unavailable" };
        }
      }),
    }),
  };
}
