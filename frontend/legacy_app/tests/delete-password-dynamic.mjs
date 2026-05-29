import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const main = fs.readFileSync(path.join(root, "js/main.js"), "utf8");

assert.match(main, /const LOGIN_ENDPOINTS = \["https:\/\/myn8n\.seommerce\.shop\/webhook\/login"\]/);
assert.match(main, /function requestDeleteCredentials\(\)/);
assert.match(main, /window\.prompt\(\s*"Digite o email da conta para confirmar a exclusão:"/s);
assert.match(main, /window\.prompt\(\s*"Digite a senha de login para eliminar produtos:"/s);
assert.match(main, /async function verifyDeleteCredentials\(email, password\)/);
assert.match(main, /postJsonWithFallback\(\s*LOGIN_ENDPOINTS,\s*\{\s*user: email,\s*email,\s*password\s*\},\s*\{\s*retryOnHttpError: false\s*\}\s*\)/s);

console.log("delete-login-auth: ok");
