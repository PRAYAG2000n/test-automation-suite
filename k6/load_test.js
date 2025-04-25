import http from "k6/http";
import { check, sleep } from "k6";
import { Trend, Rate, Counter } from "k6/metrics";

const loginMs    = new Trend("login_latency_ms");
const checkoutMs = new Trend("checkout_latency_ms");
const errRate    = new Rate("error_rate");
const orders     = new Counter("orders_placed");
const BASE = __ENV.APP_BASE_URL || "http://localhost:8000";
const hdrs = { "Content-Type": "application/json" };

export const options = {
  stages: [
    { duration: "30s", target: 100 },
    { duration: "1m",  target: 300 },
    { duration: "30s", target: 500 },   // peak
    { duration: "1m",  target: 500 },
    { duration: "30s", target: 0   },
  ],
  thresholds: {
    login_latency_ms:    ["p(95)<500"],
    checkout_latency_ms: ["p(95)<800"],
    error_rate:          ["rate<0.05"],
  },
};

export default function () {
  let t0 = Date.now();
  let res = http.post(
    `${BASE}/auth/login`,
    JSON.stringify({ username: `loaduser_${__VU}`, password: "secret_sauce" }),
    { headers: hdrs }
  );
  loginMs.add(Date.now() - t0);

  if (!check(res, { "login ok": (r) => r.status === 200 })) {
    errRate.add(1);
    sleep(1);
    return;
  }
  errRate.add(0);

  let tok = res.json("token");
  let auth = { ...hdrs, Authorization: `Bearer ${tok}` };
  http.get(`${BASE}/products`, { headers: auth });
  http.get(`${BASE}/products/1`, { headers: auth });

  //cart + checkout
  http.post(`${BASE}/cart`, JSON.stringify({ product_id: 1, qty: 1 }), { headers: auth });

  t0 = Date.now();
  let co = http.post(
    `${BASE}/checkout`,
    JSON.stringify({ first_name: "Load", last_name: "Test", zip_code: "10001" }),
    { headers: auth }
  );
  checkoutMs.add(Date.now() - t0);
  if (check(co, { "checkout ok": (r) => r.status === 200 })) {
    orders.add(1);
  }

  http.post(`${BASE}/auth/logout`, null, { headers: auth });
  sleep(1);
}
