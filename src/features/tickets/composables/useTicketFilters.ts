import { storeToRefs } from 'pinia'
import { useTicketsStore } from '../stores/tickets.store'

export function useTicketFilters() {
  const store = useTicketsStore()
  const { filters } = storeToRefs(store)

  function apply() {
    store.load()
  }

  return {
    filters,
    setFilter: store.setFilter,
    resetFilters: () => { store.resetFilters(); store.load() },
    apply,
  }
}
