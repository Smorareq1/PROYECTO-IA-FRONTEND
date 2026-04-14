import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import type { Ticket } from '../models/ticket'
import type { TicketFilters } from '../services/tickets.service'
import { getTickets } from '../services/tickets.service'

export interface PaginationMeta {
  total: number
  page: number
  size: number
  pages: number
}

export const useTicketsStore = defineStore('tickets', () => {
  const tickets = ref<Ticket[]>([])
  const selected = ref<Ticket | null>(null)
  const isLoading = ref(false)
  const pagination = ref<PaginationMeta>({ total: 0, page: 1, size: 20, pages: 0 })
  const filters = reactive<TicketFilters>({ page: 1, size: 20 })

  async function load() {
    isLoading.value = true
    try {
      const result = await getTickets(filters)
      tickets.value = result.items
      pagination.value = {
        total: result.total,
        page: result.page,
        size: result.size,
        pages: result.pages,
      }
    } finally {
      isLoading.value = false
    }
  }

  function select(ticket: Ticket | null) {
    selected.value = ticket
  }

  function setFilter(key: keyof TicketFilters, value: string | number | undefined) {
    (filters as Record<string, unknown>)[key] = value
    filters.page = 1
  }

  function resetFilters() {
    Object.assign(filters, {
      page: 1,
      size: 20,
      status: undefined,
      category: undefined,
      q: undefined,
      assignee: undefined,
    })
  }

  return { tickets, selected, isLoading, pagination, filters, load, select, setFilter, resetFilters }
})
