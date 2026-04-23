import { storeToRefs } from 'pinia'
import { useTicketsStore } from '../stores/tickets.store'

export function useTicketFilters() {
  const store = useTicketsStore()
  const { filters } = storeToRefs(store)

  function apply() {
    store.load()
  }

  function setFilter(key: Parameters<typeof store.setFilter>[0], value: Parameters<typeof store.setFilter>[1]) {
    store.setFilter(key, value)
    store.load()
  }

  return {
    filters,
    setFilter,
    resetFilters: () => { store.resetFilters(); store.load() },
    apply,
  }
}
