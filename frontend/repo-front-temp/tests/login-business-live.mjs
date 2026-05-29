import assert from "node:assert/strict";

const LOGIN_URL = "https://myn8n.seommerce.shop/webhook/login";
const EMAIL = "yasminloja89@gamil.com";
const PASSWORD = "123456";

function pickAccount(data) {
  if (Array.isArray(data)) {
    return data.find((item) => item && typeof item === "object") || null;
  }
  return data && typeof data === "object" ? data : null;
}

const res = await fetch(LOGIN_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user: EMAIL,
    email: EMAIL,
    password: PASSWORD,
  }),
});

assert.equal(res.status, 200, "login endpoint should return HTTP 200");

const account = pickAccount(await res.json());
assert.ok(account, "login response should include an account payload");
assert.equal(account.login, EMAIL);
assert.equal(account.business, true);

console.log("login-business-live: ok");
