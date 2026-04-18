import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useMetricsStore } from '../stores/metrics.store'

export function useModelMetrics() {
  const store = useMetricsStore()
  const { modelInfo, metrics, confusionMatrix, kfolds, isLoading, error } = storeToRefs(store)

  onMounted(() => {
    if (!metrics.value) store.loadAll()
  })

  return { modelInfo, metrics, confusionMatrix, kfolds, isLoading, error, reload: store.loadAll }
}
