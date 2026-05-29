import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const account = fs.readFileSync(path.join(root, "minha-conta.html"), "utf8");

assert.match(account, /id="account-save-btn"/);
assert.match(account, /id="account-cancel-btn"/);
assert.match(account, /id="account-status"/);
assert.match(account, /function setupAccountActions\(\)/);
assert.match(account, /localStorage\.setItem\("signup_name", name\)/);
assert.match(account, /localStorage\.setItem\("gp_user", email\)/);
assert.match(account, /localStorage\.setItem\("account_phone", phone\)/);
assert.match(account, /localStorage\.setItem\("account_cargo", cargo\)/);

console.log("account-settings: ok");
