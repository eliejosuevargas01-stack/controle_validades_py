import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const testsDir = path.join(root, "tests");

const tests = fs
  .readdirSync(testsDir)
  .filter((name) => name.endsWith(".mjs"))
  .sort()
  .map((name) => path.join(testsDir, name));

let failed = false;
for (const testFile of tests) {
  const result = spawnSync(process.execPath, [testFile], {
    cwd: root,
    stdio: "inherit",
  });
  if (result.status !== 0) {
    failed = true;
    break;
  }
}

if (failed) {
  process.exit(1);
}

console.log(`All ${tests.length} test script(s) passed.`);
