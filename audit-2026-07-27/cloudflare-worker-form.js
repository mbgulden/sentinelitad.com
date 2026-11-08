/**
 * Cloudflare Worker — Sentinel ITAD Lead Capture
 *
 * Replaces formsubmit.co with direct-to-inbox delivery + Turnstile spam protection.
 * Deploy to Cloudflare Workers, route at the path /api/lead on the sentinelitad-com
 * Pages project (or as a standalone Worker with a custom route).
 *
 * Required env vars / secrets (set via `wrangler secret put`):
 *   TURNSTILE_SECRET  — Cloudflare Turnstile secret key (server-side)
 *   MAIL_TO           — destination email (e.g. Michael@growthwebdev.com)
 *   MAIL_FROM         — verified sender on the zone (e.g. leads@sentinelitad.com)
 *
 * Required bindings (set in wrangler.toml):
 *   [[kv_namespaces]]
 *   binding = "RATE_LIMIT"
 *   id = "<your-kv-namespace-id>"
 *
 * Public Turnstile sitekey goes in the HTML form (not here). Get it from
 * Cloudflare Dashboard → Turnstile → your widget → "Site Key".
 *
 * DEPLOYMENT (assuming wrangler installed and authenticated):
 *   wrangler kv namespace create RATE_LIMIT
 *   wrangler secret put TURNSTILE_SECRET
 *   wrangler secret put MAIL_TO
 *   wrangler secret put MAIL_FROM
 *   wrangler deploy
 *
 * Then in the Cloudflare Pages project, add a Worker route:
 *   sentinelitad.com/api/lead  →  this-worker
 *
 * Update the HTML form action from `https://formsubmit.co/team@sentinelitad.com`
 * to `/api/lead` and add the Turnstile widget (see FORM_UPDATE_SNIPPET below).
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // CORS preflight (if you ever want to allow cross-origin POST)
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(request, env),
      });
    }

    // Only handle POST to /api/lead
    if (url.pathname !== "/api/lead") {
      return new Response("Not found", { status: 404 });
    }
    if (request.method !== "POST") {
      return new Response("Method not allowed", {
        status: 405,
        headers: { Allow: "POST" },
      });
    }

    // Origin / referer guard — only accept requests from sentinelitad.com / www.sentinelitad.com
    const origin = request.headers.get("Origin") || "";
    const referer = request.headers.get("Referer") || "";
    const allowed =
      origin.endsWith("sentinelitad.com") ||
      referer.startsWith("https://sentinelitad.com/") ||
      referer.startsWith("https://www.sentinelitad.com/");
    if (!allowed) {
      return jsonResponse({ ok: false, error: "Forbidden origin" }, 403);
    }

    // Per-IP rate limit: 5 submissions per 10 minutes (KV-backed)
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const rl = await checkRateLimit(env.RATE_LIMIT, ip, 5, 600);
    if (!rl.allowed) {
      return jsonResponse(
        { ok: false, error: "Too many requests. Please try again later." },
        429,
        { "Retry-After": String(rl.retryAfter) }
      );
    }

    // Parse form body (application/x-www-form-urlencoded or multipart/form-data)
    let form;
    try {
      form = await request.formData();
    } catch (err) {
      return jsonResponse({ ok: false, error: "Invalid form submission" }, 400);
    }

    // Extract + sanitize fields
    const data = {
      name:        sanitize(form.get("name")),
      company:     sanitize(form.get("company")),
      email:       sanitize(form.get("email")),
      phone:       sanitize(form.get("phone")),
      requestType: sanitize(form.get("request_type")),
      message:     sanitize(form.get("message")),
      turnstile:   sanitize(form.get("cf-turnstile-response")),
      page:        sanitize(form.get("page") || url.pathname),
      referer,
    };

    // Required-field validation
    const missing = [];
    if (!data.name) missing.push("name");
    if (!data.company) missing.push("company");
    if (!data.email || !isEmail(data.email)) missing.push("email");
    if (!data.message || data.message.length < 5) missing.push("message");
    if (missing.length) {
      return jsonResponse(
        { ok: false, error: "Missing or invalid: " + missing.join(", ") },
        400
      );
    }

    // Turnstile verification
    const tsOk = await verifyTurnstile(env.TURNSTILE_SECRET, data.turnstile, ip);
    if (!tsOk) {
      return jsonResponse(
        { ok: false, error: "Spam check failed. Please try again." },
        403
      );
    }

    // Compose email
    const subject = `[Sentinel ITAD] ${data.requestType || "Pickup request"} — ${data.company}`;
    const body = [
      `New lead from sentinelitad.com`,
      ``,
      `Name:          ${data.name}`,
      `Company:       ${data.company}`,
      `Email:         ${data.email}`,
      `Phone:         ${data.phone || "(none)"}`,
      `Request type:  ${data.requestType || "(none)"}`,
      `Page:          ${data.page}`,
      ``,
      `Project details:`,
      data.message,
      ``,
      `--`,
      `IP:            ${ip}`,
      `User-Agent:    ${request.headers.get("User-Agent") || "unknown"}`,
      `Submitted:     ${new Date().toISOString()}`,
    ].join("\n");

    // Send via MailChannels (free with Workers; requires SPF allowlist in zone)
    const mailResp = await sendMail(env, env.MAIL_FROM, env.MAIL_TO, subject, body, data.email);

    if (!mailResp.ok) {
      // Log for the operator; show generic error to user
      console.error("Mail send failed:", mailResp.error, JSON.stringify({ data: { ...data, message: "[redacted]" } }));
      return jsonResponse(
        { ok: false, error: "We couldn't deliver your request. Please call 808-498-1125 directly." },
        502
      );
    }

    // Redirect to /thanks.html on success
    return new Response(null, {
      status: 303,
      headers: { Location: "https://sentinelitad.com/thanks.html" },
    });
  },
};

// ----- helpers -----

function sanitize(v) {
  if (v === null || v === undefined) return "";
  return String(v).replace(/[\u0000-\u001f\u007f]/g, "").trim().slice(0, 5000);
}

function isEmail(s) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

function jsonResponse(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", ...extra },
  });
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowed =
    origin.endsWith("sentinelitad.com") ? origin : "https://sentinelitad.com";
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

async function checkRateLimit(kv, key, max, windowSec) {
  if (!kv) return { allowed: true }; // KV not bound = no limit (dev only)
  const now = Math.floor(Date.now() / 1000);
  const k = `rl:${key}`;
  const existing = (await kv.get(k, { type: "json" })) || { count: 0, resetAt: now + windowSec };
  if (now > existing.resetAt) {
    existing.count = 0;
    existing.resetAt = now + windowSec;
  }
  existing.count += 1;
  await kv.put(k, JSON.stringify(existing), { expirationTtl: windowSec });
  return {
    allowed: existing.count <= max,
    retryAfter: Math.max(0, existing.resetAt - now),
  };
}

async function verifyTurnstile(secret, token, ip) {
  if (!secret || !token) return false;
  try {
    const resp = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ secret, response: token, remoteip: ip }),
    });
    const json = await resp.json();
    return json.success === true;
  } catch (err) {
    console.error("Turnstile verify error:", err);
    return false;
  }
}

async function sendMail(env, from, to, subject, text, replyTo) {
  // MailChannels free send — requires the zone's SPF record to include _mailchannels.growthwebdev.com
  // (or _mailchannels.<your-domain>). Add this to DNS as part of deploy.
  try {
    const r = await fetch("https://api.mailchannels.net/tx/v1/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: to, name: "Sentinel Lead Inbox" }] }],
        from: { email: from, name: "Sentinel ITAD Site" },
        reply_to: { email: replyTo },
        subject,
        content: [{ type: "text/plain", value: text }],
      }),
    });
    if (!r.ok) {
      return { ok: false, error: `MailChannels HTTP ${r.status}: ${await r.text()}` };
    }
    return { ok: true };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/* -----------------------------------------------------------------------
   FORM_UPDATE_SNIPPET — paste into public/index.html (and the other pages)
   replacing the existing <form class="lead-form" action="https://formsubmit.co/team@sentinelitad.com" ...> block.

   Replace TURNSTILE_SITEKEY with your real sitekey from
   Cloudflare Dashboard → Turnstile → widget → "Site Key".

   Add the Turnstile widget <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
   in <head> (idempotent — only loads once even if included on multiple pages).
-----------------------------------------------------------------------

<form class="lead-form" action="/api/lead" method="POST">
  <input type="hidden" name="page" value="/">
  <label>Name<input name="name" required autocomplete="name"></label>
  <label>Company<input name="company" required autocomplete="organization"></label>
  <label>Email<input name="email" type="email" required autocomplete="email"></label>
  <label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
  <label>What do you have?
    <select name="request_type">
      <option>One-time pickup</option>
      <option>Recurring MSP bin / pickup route</option>
      <option>Office or server-room decommissioning</option>
      <option>Data-bearing media question</option>
    </select>
  </label>
  <label>Project details<textarea name="message" rows="5" placeholder="Example: 12 desktops, 2 rack servers, about 30 drives, Boise office, pickup this month."></textarea></label>
  <div class="cf-turnstile" data-sitekey="TURNSTILE_SITEKEY"></div>
  <button class="button primary" type="submit">Send request</button>
</form>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

-----------------------------------------------------------------------
   wrangler.toml sketch (you create this in the repo):

   name = "sentinel-lead-worker"
   main = "cloudflare-worker-form.js"
   compatibility_date = "2026-07-27"

   [[kv_namespaces]]
   binding = "RATE_LIMIT"
   id = "<from-wrangler-kv-namespace-create>"

   # Optionally pin routes if not using Pages Functions:
   # [[routes]]
   # pattern = "sentinelitad.com/api/lead"
   # zone_name = "sentinelitad.com"

-----------------------------------------------------------------------
   DNS add before MailChannels will deliver:

   Type    Name                           Value
   TXT     sentinelitad.com               "v=spf1 include:_mailchannels.growthwebdev.com ~all"
   (or whatever your zone's SPF includes — MailChannels requires your zone's SPF to include the MailChannels include for your domain.)

   If you want replies from you to come from a Sentinel-domain address (recommended),
   also set up Cloudflare Email Routing for team@sentinelitad.com → your real inbox.
----------------------------------------------------------------------- */