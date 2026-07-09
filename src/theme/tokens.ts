export const sentinelTheme = {
  name: "Sentinel Light",
  rule: "Light global theme. Dark backgrounds only inside scoped modules such as .dark, .primary, warning/status banners, and selected CTA strips.",
  colors: {
    bg: "#f7f8fb",
    surface: "#ffffff",
    surface2: "#f0f4f8",
    ink: "#111827",
    text: "#172033",
    muted: "#5b6475",
    line: "#d8e0ea",
    dark: "#071018",
    dark2: "#101923",
    darkText: "#f5f7fb",
    darkMuted: "#b9c2d2",
    teal: "#087f70",
    tealBright: "#38f2d0",
    blue: "#285fbd",
    warn: "#9a6700",
  },
  layout: {
    maxWidth: "1180px",
    pageGutter: "1rem",
    radiusCard: ".9rem",
    radiusPanel: "1.15rem",
  },
  typography: {
    body: "Inter, system-ui, -apple-system, Segoe UI, sans-serif",
    mono: "Geist Mono, monospace",
  },
} as const;

export type SentinelTheme = typeof sentinelTheme;
