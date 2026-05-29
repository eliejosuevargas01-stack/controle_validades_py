import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const server = fs.readFileSync(path.join(root, "server.py"), "utf8");

assert.match(server, /def notify_get_response\(action: Optional\[str\] = None\) -> JSONResponse:/);
assert.match(server, /@app\.get\("\/api\/notify"\)/);
assert.match(server, /@app\.get\("\/api\/notify\/\{action\}"\)/);
assert.match(server, /"message": "Use POST para disparar notify\."/);
assert.match(server, /"method": "GET"/);

console.log("notify-get-compat: ok");
