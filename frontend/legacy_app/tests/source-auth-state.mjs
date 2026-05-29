import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function read(file) {
  return fs.readFileSync(path.join(root, file), "utf8");
}

const login = read("login.html");
const checkout = read("checkout.html");
const signup = read("signup.html");
const account = read("minha-conta.html");
const main = read("js/main.js");

assert.match(login, /gp_account_business/);
assert.match(login, /persistAccountState/);
assert.match(login, /localStorage\.setItem\(PLAN_KEY, businessFlag \? PLAN_BUSINESS : PLAN_FREE\)/);

assert.match(checkout, /gp_account_business/);
assert.match(checkout, /localStorage\.setItem\("plan_type", "business"\)/);

assert.match(signup, /localStorage\.setItem\("gp_account_business", "0"\)/);
assert.match(signup, /localStorage\.setItem\("plan_type", "free"\)/);

assert.match(account, /gp_account_business/);
assert.match(account, /planType/);
assert.match(account, /account-save-btn/);
assert.match(account, /localStorage\.setItem\("account_phone"/);
assert.match(account, /localStorage\.setItem\("account_cargo"/);

assert.match(main, /ACCOUNT_BUSINESS_KEY = "gp_account_business"/);
assert.match(main, /function getPlanType\(\)/);
assert.match(main, /localStorage\.setItem\(PLAN_KEY, isBusiness \? PLAN_BUSINESS : PLAN_FREE\)/);
assert.match(main, /function requestDeleteCredentials\(\)/);
assert.match(main, /async function verifyDeleteCredentials\(email, password\)/);

console.log("source-auth-state: ok");
