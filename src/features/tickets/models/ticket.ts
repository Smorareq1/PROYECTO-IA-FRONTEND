import type { Category, TicketStatus } from '@/core/config/constants'

export type { Category, TicketStatus }

export interface Ticket {
  id: string
  subject: string
  description: string
  predicted_category: Category
  confidences: Record<Category, number>
  final_category: Category | null
  status: TicketStatus
  created_by: string
  assignee_id: string | null
  created_at: string
  updated_at: string
}

export interface CreateTicketDto {
  subject: string
  description: string
}

export interface UpdateTicketDto {
  status?: TicketStatus
  final_category?: Category
  assignee_id?: string
}
