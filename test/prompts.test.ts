import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { expect, it } from "vitest";
import { PROMPT_WORDS } from "./words.js";
import { typed } from "./pi.js";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const manifest = () => JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8")) as { comchatx: { prompts: Record<string, { zh: string }> } };

it("each template expands in a pi session: its arguments and the seller's own words reach the model, no placeholder does", async () => {
  const expected: Record<string, [string, string]> = {
    "stock-position": ["/stock-position 只看美国站", `${PROMPT_WORDS["stock-position"].body} 只看美国站`],
    "restock-plan": ["/restock-plan US,DE 海运", `${PROMPT_WORDS["restock-plan"].body} US,DE 海运`],
    "stock-cost": ["/stock-cost", `${PROMPT_WORDS["stock-cost"].body}`],
    "stuck-stock": ["/stuck-stock SKU-1", `${PROMPT_WORDS["stuck-stock"].body} SKU-1`],
    "stockout-review": ["/stockout-review 2026-10-01..2026-10-31", `${PROMPT_WORDS["stockout-review"].body} 2026-10-01..2026-10-31`],
  };
  expect(Object.keys(expected).sort()).toEqual(Object.keys(manifest().comchatx.prompts).sort());
  for (const [name, [input, text]] of Object.entries(expected)) {
    const received = await typed(ROOT, input);
    expect(received.trim(), name).toBe(text);
    expect(received, name).not.toMatch(/\$\{?[@0-9A]/);
  }
}, 120_000);

