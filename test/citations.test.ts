import { readFileSync, readdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { expect, it } from "vitest";
import { body } from "./pi.js";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const README = readFileSync(join(ROOT, "research", "README.md"), "utf8");
const ID = /[WCORISFGTAQ]\d+/g;
const GROUP = /\(([WCORISFGTAQ]\d+(?:\s*[,;]\s*[WCORISFGTAQ]\d+)*)\)/g;

const section = (from: string, to: string): string => README.slice(README.indexOf(from), README.indexOf(to, README.indexOf(from)));
const POSITIONS = section("## Positions the skills will take", "### The seat's own");
const SEATS = section("### The seat's own", "## Where the files disagreed");

/** Every position Jack passed, as `research/README.md` opens it: `- **<letter><n>.**` at the head of a list entry. */
const positions = new Set([...POSITIONS.matchAll(/^- \*\*([WCORISFGTAQ]\d+)\.\*\*/gm)].map((match) => match[1]!));

/** The seat's own lines: no source, so no skill rests on them; each with words that would restate its claim. */
const SEAT_CLAIMS = [
  /fault of the read/i,
  /count(?:s|ed)? the same units twice/i,
  /errs both ways/i,
  /one convention/i,
  /demand spike alone/i,
  /not yet a loss|timeout rather than a count/i,
  /most likely Amazon's automated/i,
  /names only the `?DEFAULT`?[^.]*drops/i,
  /two of the three fees/i,
  /argument for stating settings/i,
] as const;

const markdown = (directory: string): string[] =>
  readdirSync(directory, { recursive: true, encoding: "utf8" }).filter((file) => file.endsWith(".md")).map((file) => join(directory, file));

/** A line that only points: to a reference, another skill, the door's reference or the research. */
const pointer = (line: string) => /references\/[\w-]+\.md|\.\.\/[\w-]+\/SKILL\.md|research\//.test(line);

const lines = markdown(join(ROOT, "skills")).flatMap((file) =>
  body(readFileSync(file, "utf8"))
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line !== "" && !line.startsWith("#") && !/^\|?[-:| ]+\|?$/.test(line))
    .map((line) => ({ file, line, ids: [...line.matchAll(GROUP)].flatMap((group) => group[1]!.match(ID) ?? []) })),
);

it("the research holds the 283 positions Jack passed, by letter, and ten lines of the seat's own that carry no id", () => {
  const count = (letter: string) => [...positions].filter((id) => id.startsWith(letter)).length;
  expect(Object.fromEntries([..."WCORISFGTAQ"].map((letter) => [letter, count(letter)]))).toEqual({ W: 46, C: 44, O: 32, R: 34, I: 26, S: 30, F: 32, G: 25, T: 5, A: 5, Q: 4 });
  expect(positions.size).toBe(283);
  const seats = SEATS.split("\n").filter((line) => line.startsWith("- "));
  expect(seats).toHaveLength(10);
  for (const line of seats) expect(line.match(/\*\*[WCORISFGTAQ]\d+\.\*\*/), line).toBeNull();
  SEAT_CLAIMS.forEach((claim, n) => expect(claim.test(seats[n]!), `seat line ${n + 1}`).toBe(true));
});

it("every line of the skills and their references cites a position that exists, except a line that only points", () => {
  expect(lines.length).toBeGreaterThan(0);
  for (const { file, line, ids } of lines) {
    if (ids.length === 0) expect(pointer(line), `${file}: ${line}`).toBe(true);
    for (const id of ids) expect(positions.has(id), `${file}: ${id}`).toBe(true);
  }
});

it("each of the 283 positions is cited somewhere in the skills", () => {
  const cited = new Set(lines.flatMap(({ ids }) => ids));
  expect([...positions].filter((id) => !cited.has(id))).toEqual([]);
});

it("no line of the skills restates a claim of the seat's own", () => {
  for (const { file, line } of lines) for (const claim of SEAT_CLAIMS) expect(claim.test(line), `${file}: ${line}`).toBe(false);
});

it("the citation check fails a line citing a position that does not exist, and one citing nothing", () => {
  const check = (line: string) => {
    const ids = [...line.matchAll(GROUP)].flatMap((group) => group[1]!.match(ID) ?? []);
    return ids.length === 0 ? pointer(line) : ids.every((id) => positions.has(id));
  };
  expect(check("Fulfillable units can be bought now (W1).")).toBe(true);
  expect(check("Fulfillable units can be bought now (W99).")).toBe(false);
  expect(check("Fulfillable units can be bought now.")).toBe(false);
  expect(check("[reads-and-roles.md](references/reads-and-roles.md): every read and its role.")).toBe(true);
});
