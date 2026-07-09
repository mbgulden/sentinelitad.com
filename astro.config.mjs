import { defineConfig } from "astro/config";

const integrations = [];

// EmDash is intentionally gated so static preview/builds keep working without a
// local database or Cloudflare bindings. Production CMS deployments should set
// ENABLE_EMDASH=true and provide the database/storage bindings documented in
// docs/theme/emdash-integration.md.
if (process.env.ENABLE_EMDASH === "true") {
  const { default: emdash } = await import("emdash/astro");
  const { sqlite } = await import("emdash/db");

  integrations.push(
    emdash({
      database: sqlite({
        url: process.env.EMDASH_SQLITE_URL ?? "file:./.emdash/sentinelitad.db",
      }),
    }),
  );
}

export default defineConfig({
  site: "https://sentinelitad.com",
  output: process.env.ENABLE_EMDASH === "true" ? "server" : "static",
  integrations,
});
