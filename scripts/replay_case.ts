// D17 replay harness against the REAL runtime.
// Usage: node --experimental-strip-types scripts/replay_case.ts <case.json>
// where case.json matches TicketPayload. Local runs need AI_GATEWAY_API_KEY
// (Vercel deploys use OIDC and need no key). Lookup tools degrade gracefully
// if SUPPORT_DB_READONLY_URL / STRIPE_RESTRICTED_KEY are absent — the agent
// sees the error and should list lookups_needed instead of guessing.

import { readFileSync } from "node:fs";
import { runDraftAgent } from "../agent/run.ts";

const path = process.argv[2];
if (!path) {
  console.error("usage: npm run replay -- <case.json>");
  process.exit(1);
}

// minimal .env loader so local replay works without extra deps
try {
  for (const line of readFileSync(".env", "utf8").split("\n")) {
    const m = line.match(/^([A-Z_]+)=(.*)$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].split(" #")[0].trim();
  }
} catch {}

const payload = JSON.parse(readFileSync(path, "utf8"));
const result = await runDraftAgent(payload);
console.log(JSON.stringify(result, null, 2));
