import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { expect, it } from "vitest";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));

/** The forms it holds: `/Users/<name>/`, `/home/<name>/` and `C:\Users\<name>\` with an ASCII name, not preceded by a word character, a dot, a colon, a slash or a hyphen (so a URL's `/home/` segment and a `file://` URI pass). */
const HOME = /(?<![\w.:/-])\/(?:Users|home)\/[A-Za-z0-9._-]+\/|\b[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\/;

const SELF = "test/privacy.test.ts";

const tracked = (): string[] => execFileSync("git", ["ls-files", "-z"], { cwd: ROOT, encoding: "utf8" }).split("\0").filter(Boolean);

/** The lines of the given files, the test itself by its full path skipped, that name a home path. */
const homes = (files: readonly string[], read: (file: string) => string): string[] =>
  files
    .filter((file) => file !== SELF)
    .flatMap((file) => read(file).split("\n").map((line, n) => [file, n + 1, line] as const))
    .filter(([, , line]) => HOME.test(line))
    .map(([file, n]) => `${file}:${n}`);

it("no tracked file names a path in a home directory on a machine", () => {
  const files = tracked();
  expect(files.length).toBeGreaterThan(0);
  expect(files).toContain("package-lock.json");
  expect(homes(files, (file) => readFileSync(join(ROOT, file), "utf8"))).toEqual([]);
});

it("the scan reads the lockfile and any other file named privacy.test.ts: a home path in either is caught", () => {
  const planted: Record<string, string> = {
    "package-lock.json": '{\n  "resolved": "/Users/someone/project/models/x.tgz"\n}',
    "research/fixtures/test/privacy.test.ts": 'const at = "/home/someone/clone";',
  };
  expect(homes(Object.keys(planted), (file) => planted[file]!)).toEqual(["package-lock.json:2", "research/fixtures/test/privacy.test.ts:1"]);
});

it("the home check catches a home path and passes a URL with a home segment", () => {
  for (const line of ["read at /Users/someone/project/models/", "see /home/dev/clone", "C:\\Users\\someone\\Desktop"]) expect(HOME.test(line), line).toBe(true);
  for (const line of ["https://www.khoury.northeastern.edu/home/cbw/static/pdf/x.pdf", "a local clone of `amzn/selling-partner-api-models`"]) expect(HOME.test(line), line).toBe(false);
});
