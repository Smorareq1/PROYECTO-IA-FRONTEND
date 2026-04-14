import { ref } from 'vue'
import { createTicket, updateTicket, deleteTicket } from '../services/tickets.service'
import { useTicketsStore } from '../stores/tickets.store'
import { handleError } from '@/core/errors/handler'
import { useToast } from '@/core/composables/useToast'
import type { CreateTicketDto, UpdateTicketDto, Ticket } from '../models/ticket'

export function useTicketMutations() {
  const store = useTicketsStore()
  const toast = useToast()
  const isSubmitting = ref(false)

  async function create(dto: CreateTicketDto): Promise<Ticket | null> {
    isSubmitting.value = true
    try {
      const ticket = await createTicket(dto)
      toast.success('Ticket creado', `${ticket.id} fue clasificado exitosamente.`)
      return ticket
    } catch (e) {
      handleError(e)
      return null
    } finally {
      isSubmitting.value = false
    }
  }

  async function update(id: string, dto: UpdateTicketDto): Promise<Ticket | null> {
    isSubmitting.value = true
    try {
      const ticket = await updateTicket(id, dto)
      await store.load()
      toast.success('Ticket actualizado')
      return ticket
    } catch (e) {
      handleError(e)
      return null
    } finally {
      isSubmitting.value = false
    }
  }

  async function remove(id: string): Promise<void> {
    try {
      await deleteTicket(id)
      await store.load()
      toast.success('Ticket eliminado')
    } catch (e) {
      handleError(e)
    }
  }

  return { create, update, remove, isSubmitting }
}
