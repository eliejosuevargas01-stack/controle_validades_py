import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function read(file) {
  return fs.readFileSync(path.join(root, file), "utf8");
}

const main = read("main.js");
const login = read("login.html");
const signup = read("signup.html");
const checkout = read("checkout.html");

assert.match(main, /postJsonWithFallback\(getEndpoints\("produto"\), payload, \{ retryOnHttpError: false \}\)/);
assert.match(main, /postJsonWithFallback\(getEndpoints\("actions"\), payload, \{ retryOnHttpError: false \}\)/);
assert.match(main, /window\.prompt\(\s*"Digite o email da conta para confirmar a exclusão:"/s);
assert.match(main, /window\.prompt\(\s*"Digite a senha de login para eliminar produtos:"/s);
assert.match(main, /action: "apagar",\s*\.\.\.payload,\s*id: idVal,\s*password: credentials\.password,\s*\.\.\.getUserPayloadForEmail\(credentials\.email\)/s);
assert.match(main, /async function verifyDeleteCredentials\(email, password\)/);

assert.match(login, /postJsonWithFallback\(LOGIN_ENDPOINTS, \{\s*user: email,/s);
assert.match(login, /retryOnHttpError: false/);
assert.match(signup, /retryOnHttpError: false/);
assert.match(checkout, /retryOnHttpError: false/);

console.log("source-write-guards: ok");
