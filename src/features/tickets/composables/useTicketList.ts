import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useTicketsStore } from '../stores/tickets.store'

export function useTicketList() {
  const store = useTicketsStore()
  const { tickets, isLoading, pagination } = storeToRefs(store)

  onMounted(() => store.load())

  return {
    tickets,
    isLoading,
    pagination,
    reload: () => store.load(),
    select: store.select,
  }
}
