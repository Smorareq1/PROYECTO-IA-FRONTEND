import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Role } from '@/core/config/constants'
import { hasTokens, clearTokens } from '@/core/auth/token-storage'

export interface SessionUser {
  id: string
  email: string
  full_name: string
  role: Role
}

/**
 * Auth store — lives in core so design-system and guards can import it.
 * Business logic (API calls) stays in features/auth/services.
 */
export const useAuthStore = defineStore('auth', () => {
  const user = ref<SessionUser | null>(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!user.value && hasTokens())
  const role = computed<Role | null>(() => user.value?.role ?? null)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isAgent = computed(() => user.value?.role === 'agente' || user.value?.role === 'admin')
  const isClient = computed(() => user.value?.role === 'cliente')

  function setUser(u: SessionUser | null) {
    user.value = u
  }

  function logout() {
    user.value = null
    clearTokens()
  }

  return {
    user,
    isLoading,
    isAuthenticated,
    role,
    isAdmin,
    isAgent,
    isClient,
    setUser,
    logout,
  }
}, {
  persist: {
    pick: ['user'],
  },
})
