export const sentinelTheme = {
  name: "Secure Current",
  rule: "Light global theme. Dark navy backgrounds only inside scoped modules such as .dark panels and .primary CTAs. Color lives in sections, callouts, and accents.",
  colors: {
    bg: "#F7FAFB",
    surface: "#ffffff",
    surface2: "#DCE9EC",
    ink: "#071A2B",
    text: "#163B52",
    muted: "#54708A",
    line: "#C9D8DE",
    dark: "#071A2B",
    dark2: "#0E2438",
    darkText: "#F7FAFB",
    darkMuted: "#A9C3D1",
    brand: "#163B52",
    brandBright: "#3CC2D3",
    brandInk: "#F7FAFB",
    accent: "#3CC2D3",
    warn: "#9a6700",
    logoPrimary: "#1B3A5C",
  },
  layout: {
    maxWidth: "1180px",
    pageGutter: "1rem",
    radiusCard: ".9rem",
    radiusPanel: "1.15rem",
  },
  typography: {
    body: "IBM Plex Sans, system-ui, -apple-system, Segoe UI, sans-serif",
    display: "Sora, IBM Plex Sans, system-ui, sans-serif",
    mono: "IBM Plex Mono, ui-monospace, monospace",
  },
} as const;

export type SentinelTheme = typeof sentinelTheme;
