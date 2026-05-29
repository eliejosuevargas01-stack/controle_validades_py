import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const main = fs.readFileSync(path.join(root, "main.js"), "utf8");

assert.match(main, /async function deleteTargets\(targets\)/);
assert.match(main, /const credentials = requestDeleteCredentials\(\);/);
assert.match(main, /const loginCheck = await verifyDeleteCredentials\(credentials\.email, credentials\.password\);/);
assert.match(main, /action: "apagar",\s*\.\.\.payload,\s*id: idVal,\s*password: credentials\.password,\s*\.\.\.getUserPayloadForEmail\(credentials\.email\)/s);
assert.match(main, /setBulkButtonsDisabled\(true\);/);
assert.match(main, /Solicitação de eliminação enviada para/);

console.log("delete-flow-payload: ok");
