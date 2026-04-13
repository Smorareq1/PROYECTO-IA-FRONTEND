import { ref, reactive, type Ref } from 'vue'

/**
 * Composable for managing async operations with loading/error/data states
 */
export function useAsyncState<T>(defaultValue: T) {
  const data: Ref<T> = ref(defaultValue) as Ref<T>
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function execute(fn: () => Promise<T>) {
    isLoading.value = true
    error.value = null
    try {
      data.value = await fn()
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error desconocido'
    } finally {
      isLoading.value = false
    }
  }

  function reset() {
    data.value = defaultValue
    error.value = null
    isLoading.value = false
  }

  return {
    data,
    isLoading,
    error,
    execute,
    reset,
  }
}
