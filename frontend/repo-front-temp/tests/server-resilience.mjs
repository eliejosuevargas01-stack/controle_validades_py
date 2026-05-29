import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const server = fs.readFileSync(path.join(root, "server.py"), "utf8");

assert.match(server, /async def close_db_pool\(\) -> None:/);
assert.match(server, /async def ensure_db_pool\(\) -> bool:/);
assert.match(server, /Falha ao inicializar o pool do banco no startup/);
assert.match(server, /async def fetch_table_rows\(\) -> list\[dict\]:/);
assert.match(server, /db_ready": db_pool is not None/);
assert.match(server, /@app\.get\("\/api\/notify"\)/);
assert.match(server, /@app\.get\("\/api\/notify\/\{action\}"\)/);

console.log("server-resilience: ok");
