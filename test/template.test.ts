import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { expect, it } from "vitest";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const TEMPLATE = "comchatx/cx-package-template";

/** The repository this checkout is: GitHub's own name for it in CI, else the origin remote's. */
const repository = (): string => {
  if (process.env["GITHUB_REPOSITORY"]) return process.env["GITHUB_REPOSITORY"];
  try {
    return execFileSync("git", ["config", "--get", "remote.origin.url"], { cwd: ROOT, encoding: "utf8" }).trim().replace(/^.*github\.com[:/]/, "").replace(/\.git$/, "");
  } catch {
    return "";
  }
};

const walk = (directory: string): string[] => readdirSync(directory, { withFileTypes: true })
  .flatMap((entry) => (entry.name === "node_modules" || entry.name === ".git" ? [] : entry.isDirectory() ? walk(join(directory, entry.name)) : [join(directory, entry.name)]));

// A repository made from the template fails here until every placeholder is replaced. The template's own repository holds them.
it.skipIf(repository() === TEMPLATE)("holds no placeholder of the template", () => {
  const left = walk(ROOT)
    .filter((path) => !path.endsWith("test/template.test.ts") && !path.endsWith("package-lock.json"))
    .flatMap((path) => readFileSync(path, "utf8").split("\n").map((line, n) => [relative(ROOT, path), n + 1, line] as const))
    .filter(([, , line]) => /REPLACE|replace-me/.test(line))
    .map(([path, n]) => `${path}:${n}`);
  expect(left).toEqual([]);
  const field = (JSON.parse(readFileSync(join(ROOT, "package.json"), "utf8")) as { comchatx: { order: number } }).comchatx;
  expect(field.order, "comchatx.order").toBeGreaterThan(0);
});
