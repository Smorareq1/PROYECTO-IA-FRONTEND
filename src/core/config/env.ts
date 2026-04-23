import { z } from 'zod'

/**
 * Environment variables validated with Zod
 */
const envSchema = z.object({
  VITE_API_BASE_URL: z.string().default('/api/v1'),
  VITE_APP_TITLE: z.string().default('TicketAI — Mesa de Ayuda Inteligente'),
  MODE: z.enum(['development', 'production', 'test']).default('development'),
})

function parseEnv() {
  const result = envSchema.safeParse({
    VITE_API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
    VITE_APP_TITLE: import.meta.env.VITE_APP_TITLE,
    MODE: import.meta.env.MODE,
  })

  if (!result.success) {
    console.warn('⚠️ Environment validation warnings:', result.error.flatten())
    return envSchema.parse({})
  }

  return result.data
}

export const env = parseEnv()
