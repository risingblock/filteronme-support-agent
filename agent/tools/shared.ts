// Shared plumbing for the D20 tool whitelist.
//
// Every tool is a deterministic, read-only wrapper around one fixed query.
// Guards live HERE, in code — never in the prompt:
//   - email params must appear in the ticket (allowedEmails, enforced below)
//   - every call is audit-logged with the ticket reference
//   - responses are shaped; no raw API/DB objects reach the model

import mysql from "mysql2/promise";

export interface RunContext {
  ticketRef: string;
  /** lowercase emails that appear in the ticket (From + body) — the only
   *  values tools will accept as email inputs */
  allowedEmails: Set<string>;
}

export class EmailNotInTicketError extends Error {
  constructor(email: string) {
    super(
      `Rejected: "${email}" does not appear in this ticket. Tools only accept ` +
        `email addresses from the ticket itself. This guard is enforced in code.`,
    );
  }
}

export function assertAllowedEmail(ctx: RunContext, email: string): string {
  const normalized = email.trim().toLowerCase();
  if (!ctx.allowedEmails.has(normalized)) throw new EmailNotInTicketError(email);
  return normalized;
}

export function audit(
  ctx: RunContext,
  tool: string,
  input: unknown,
  outcome: "ok" | "error",
  ms: number,
): void {
  // One JSON line per call; Vercel Observability picks these up.
  console.log(
    JSON.stringify({ t: "agent_tool_call", ticketRef: ctx.ticketRef, tool, input, outcome, ms }),
  );
}

/** Wrap a tool execute() with audit logging + error shaping. */
export function instrumented<I, O>(
  ctx: RunContext,
  name: string,
  fn: (input: I) => Promise<O>,
): (input: I) => Promise<O | { error: string }> {
  return async (input: I) => {
    const start = Date.now();
    try {
      const out = await fn(input);
      audit(ctx, name, input, "ok", Date.now() - start);
      return out;
    } catch (err) {
      audit(ctx, name, input, "error", Date.now() - start);
      // Errors are returned as data so the model can adapt (e.g. escalate),
      // never thrown into the loop.
      return { error: err instanceof Error ? err.message : "lookup failed" };
    }
  };
}

// --- read-only MySQL (PlanetScale) ---
// SUPPORT_DB_READONLY_URL is a PlanetScale connection string created with a
// READ-ONLY password (dashboard → database → Passwords → role: read-only).
// The read-only-ness is enforced by PlanetScale, not by this code.

let pool: mysql.Pool | undefined;

export function db(): mysql.Pool {
  if (!pool) {
    const url = process.env.SUPPORT_DB_READONLY_URL;
    if (!url) throw new Error("SUPPORT_DB_READONLY_URL is not configured");
    pool = mysql.createPool({
      uri: url,
      connectionLimit: 2,
      ssl: { rejectUnauthorized: true }, // PlanetScale requires TLS
    });
  }
  return pool;
}

export async function queryRows(sql: string, params: unknown[]): Promise<any[]> {
  const [rows] = await db().query(sql, params);
  return rows as any[];
}

// --- Stripe REST via restricted read-only key (rk_...) ---

export async function stripeGet(
  path: string,
  params: Record<string, string>,
): Promise<any> {
  const key = process.env.STRIPE_RESTRICTED_KEY;
  if (!key) throw new Error("STRIPE_RESTRICTED_KEY is not configured");
  if (!key.startsWith("rk_")) throw new Error("Refusing non-restricted Stripe key");
  const qs = new URLSearchParams(params).toString();
  const res = await fetch(`https://api.stripe.com/v1${path}?${qs}`, {
    headers: { Authorization: `Bearer ${key}` },
  });
  if (!res.ok) throw new Error(`Stripe ${res.status} on ${path}`);
  return res.json();
}

/** Show a@b.com as a***@b.com — used when a looked-up email differs from the
 *  ticket's, so drafts never leak a full address the customer didn't provide. */
export function censorEmail(email: string): string {
  const [local, domain] = email.split("@");
  if (!domain) return "***";
  return `${local.slice(0, 1)}***@${domain}`;
}
