import { z } from 'zod'

export const createTicketSchema = z.object({
  subject: z
    .string()
    .min(5, 'El asunto debe tener al menos 5 caracteres')
    .max(200, 'Máximo 200 caracteres'),
  description: z
    .string()
    .min(20, 'Describe el problema con al menos 20 caracteres')
    .max(2000, 'Máximo 2000 caracteres'),
})

export type CreateTicketForm = z.infer<typeof createTicketSchema>
