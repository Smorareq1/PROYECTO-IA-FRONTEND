import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAnalyticsStore } from '../stores/analytics.store'

export function useModelMetrics() {
  const store = useAnalyticsStore()
  const { modelInfo, metrics, confusionMatrix, kfolds, isLoading, error } = storeToRefs(store)

  onMounted(() => {
    if (!metrics.value) store.loadAll()
  })

  return { modelInfo, metrics, confusionMatrix, kfolds, isLoading, error, reload: store.loadAll }
}
