import { defineCollection, z } from "astro:content";

const ctaSchema = z.object({ label: z.string(), href: z.string(), variant: z.enum(["primary", "secondary"]).default("primary") });
const cardSchema = z.object({ title: z.string(), body: z.string(), href: z.string().optional() });
const stepSchema = z.object({ title: z.string(), body: z.string() });

const pages = defineCollection({
  type: "data",
  schema: z.object({
    title: z.string(),
    description: z.string(),
    slug: z.string(),
    navLabel: z.string().optional(),
    hero: z.object({ eyebrow: z.string(), title: z.string(), body: z.string(), image: z.string().optional(), imageAlt: z.string().optional(), ctas: z.array(ctaSchema).default([]) }),
    warning: z.object({ strong: z.string(), body: z.string() }).optional(),
    cards: z.array(cardSchema).default([]),
    trustItems: z.array(cardSchema).default([]),
    steps: z.array(stepSchema).default([]),
    primaryCta: z.object({ eyebrow: z.string(), title: z.string(), body: z.string(), ctas: z.array(ctaSchema).default([]) }).optional(),
  }),
});

export const collections = { pages };
