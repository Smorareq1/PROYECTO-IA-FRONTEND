import { ref } from 'vue'
import { predict } from '../services/classifier.service'
import { usePlaygroundStore } from '../stores/playground.store'
import { handleError } from '@/core/errors/handler'
import type { Prediction } from '../models/prediction'

export function usePredict() {
  const store = usePlaygroundStore()
  const isLoading = ref(false)
  const result = ref<Prediction | null>(null)

  async function classify(text: string): Promise<Prediction | null> {
    if (!text.trim()) return null
    isLoading.value = true
    result.value = null
    try {
      const prediction = await predict(text)
      result.value = prediction
      store.addEntry(text, prediction)
      return prediction
    } catch (e) {
      handleError(e)
      return null
    } finally {
      isLoading.value = false
    }
  }

  function reset() {
    result.value = null
  }

  return { classify, reset, isLoading, result }
}
