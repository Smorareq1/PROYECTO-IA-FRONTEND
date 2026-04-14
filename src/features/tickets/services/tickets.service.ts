import { apiClient } from '@/core/api/client'
import type { Ticket, CreateTicketDto, UpdateTicketDto } from '../models/ticket'
import type { Paginated } from '@/core/api/types'
import { USE_MOCK } from '@/mockupdata'
import * as mock from '@/mockupdata/services/tickets.mock'

export interface TicketFilters {
  status?: string
  category?: string
  q?: string
  page?: number
  size?: number
  assignee?: string
}

export async function getTickets(filters: TicketFilters = {}): Promise<Paginated<Ticket>> {
  if (USE_MOCK) return mock.getTickets(filters)
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== ''),
  )
  const { data } = await apiClient.get<Paginated<Ticket>>('/tickets', { params })
  return data
}

export async function getTicket(id: string): Promise<Ticket> {
  if (USE_MOCK) return mock.getTicket(id)
  const { data } = await apiClient.get<Ticket>(`/tickets/${id}`)
  return data
}

export async function createTicket(dto: CreateTicketDto): Promise<Ticket> {
  if (USE_MOCK) return mock.createTicket(dto)
  const { data } = await apiClient.post<Ticket>('/tickets', dto)
  return data
}

export async function updateTicket(id: string, dto: UpdateTicketDto): Promise<Ticket> {
  if (USE_MOCK) return mock.updateTicket(id, dto)
  const { data } = await apiClient.patch<Ticket>(`/tickets/${id}`, dto)
  return data
}

export async function deleteTicket(id: string): Promise<void> {
  if (USE_MOCK) return mock.deleteTicket(id)
  await apiClient.delete(`/tickets/${id}`)
}
