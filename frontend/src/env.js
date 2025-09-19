import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  /**
   * Server-side environment variables schema.
   */
  server: {
    DATABASE_URL: z.string().url(),
    BETTER_AUTH_SECRET: z.string(),
    NODE_ENV: z
      .enum(["development", "test", "production"])
      .default("development"),

    // Storage (Cloudflare R2)
    R2_ACCESS_TOKEN: z.string(),
    R2_ACCESS_KEY_ID: z.string(),
    R2_SECRET_ACCESS_KEY: z.string(),
    R2_ENDPOINT_URL: z.string().url(),
    R2_BUCKET_NAME: z.string(),
    R2_CUSTOM_DOMAIN: z.string().url(),
    R2_REGION: z.string(),

    // Modal endpoints
    API_BEARER_TOKEN: z.string(),
    GENERATE_FROM_DESCRIPTION: z.string().url(),
    GENERATE_FROM_DESCRIBED_LYRICS: z.string().url(),
    GENERATE_WITH_LYRICS: z.string().url(),

    // Polar.sh
    POLAR_ACCESS_TOKEN: z.string(),
    POLAR_WEBHOOK_SECRET: z.string(),
  },

  /**
   * Client-side environment variables (exposed with NEXT_PUBLIC_ prefix)
   */
  client: {
    // Example: NEXT_PUBLIC_API_URL: z.string().url(),
  },

  /**
   * Map runtime env variables from process.env
   */
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET,
    NODE_ENV: process.env.NODE_ENV,

    R2_ACCESS_TOKEN: process.env.R2_ACCESS_TOKEN,
    R2_ACCESS_KEY_ID: process.env.R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY: process.env.R2_SECRET_ACCESS_KEY,
    R2_ENDPOINT_URL: process.env.R2_ENDPOINT_URL,
    R2_BUCKET_NAME: process.env.R2_BUCKET_NAME,
    R2_CUSTOM_DOMAIN: process.env.R2_CUSTOM_DOMAIN,
    R2_REGION: process.env.R2_REGION,

    API_BEARER_TOKEN: process.env.API_BEARER_TOKEN,
    GENERATE_FROM_DESCRIPTION: process.env.GENERATE_FROM_DESCRIPTION,
    GENERATE_FROM_DESCRIBED_LYRICS: process.env.GENERATE_FROM_DESCRIBED_LYRICS,
    GENERATE_WITH_LYRICS: process.env.GENERATE_WITH_LYRICS,

    POLAR_ACCESS_TOKEN: process.env.POLAR_ACCESS_TOKEN,
    POLAR_WEBHOOK_SECRET: process.env.POLAR_WEBHOOK_SECRET,
  },

  /**
   * Optional: skip validation (useful in Docker builds)
   */
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
