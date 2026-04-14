import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/core/stores/auth.store'
import { login as loginService } from '../services/auth.service'
import type { LoginCredentials } from '../models/credentials.schema'

export function useLogin() {
  const authStore = useAuthStore()
  const router = useRouter()
  const errorMessage = ref('')
  const isLoading = ref(false)

  async function login(credentials: LoginCredentials) {
    errorMessage.value = ''
    isLoading.value = true
    try {
      const response = await loginService(credentials)
      authStore.setUser(response.user)

      const role = authStore.role
      if (role === 'cliente') {
        router.push('/app/mis-tickets')
      } else if (role === 'agente') {
        router.push('/app/cola')
      } else {
        router.push('/app/dashboard')
      }
    } catch {
      errorMessage.value = 'Credenciales incorrectas. Intenta de nuevo.'
    } finally {
      isLoading.value = false
    }
  }

  return { login, errorMessage, isLoading }
}
