import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/core/stores/auth.store'

export function useCurrentUser() {
  const store = useAuthStore()
  const { user, role, isAuthenticated, isAdmin, isAgent, isClient } = storeToRefs(store)
  return { user, role, isAuthenticated, isAdmin, isAgent, isClient }
}
