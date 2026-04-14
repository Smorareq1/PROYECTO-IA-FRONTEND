import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ModelMetrics, ConfusionMatrix, ModelInfo } from '../models/metrics'
import type { KFoldReport } from '../models/kfold'
import { getModelInfo, getMetrics, getConfusionMatrix, getKFolds } from '../services/metrics.service'

export const useMetricsStore = defineStore('metrics', () => {
  const modelInfo = ref<ModelInfo | null>(null)
  const metrics = ref<ModelMetrics | null>(null)
  const confusionMatrix = ref<ConfusionMatrix | null>(null)
  const kfolds = ref<KFoldReport | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function loadAll() {
    isLoading.value = true
    error.value = null
    try {
      const [info, m, cm, kf] = await Promise.all([
        getModelInfo(),
        getMetrics(),
        getConfusionMatrix(),
        getKFolds(),
      ])
      modelInfo.value = info
      metrics.value = m
      confusionMatrix.value = cm
      kfolds.value = kf
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Error cargando métricas'
    } finally {
      isLoading.value = false
    }
  }

  return { modelInfo, metrics, confusionMatrix, kfolds, isLoading, error, loadAll }
})
