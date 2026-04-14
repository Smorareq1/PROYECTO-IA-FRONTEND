import { apiClient } from '@/core/api/client'
import type { ModelMetrics, ConfusionMatrix, ModelInfo, TopWord } from '../models/metrics'
import type { KFoldReport } from '../models/kfold'
import type { Category } from '@/core/config/constants'
import { USE_MOCK } from '@/mockupdata'
import * as mock from '@/mockupdata/services/analytics.mock'

export async function getModelInfo(): Promise<ModelInfo> {
  if (USE_MOCK) return mock.getModelInfo()
  const { data } = await apiClient.get<ModelInfo>('/model/info')
  return data
}

export async function getMetrics(): Promise<ModelMetrics> {
  if (USE_MOCK) return mock.getMetrics()
  const { data } = await apiClient.get<ModelMetrics>('/model/metrics')
  return data
}

export async function getConfusionMatrix(): Promise<ConfusionMatrix> {
  if (USE_MOCK) return mock.getConfusionMatrix()
  const { data } = await apiClient.get<ConfusionMatrix>('/model/confusion-matrix')
  return data
}

export async function getKFolds(): Promise<KFoldReport> {
  if (USE_MOCK) return mock.getKFolds()
  const { data } = await apiClient.get<KFoldReport>('/model/kfolds')
  return data
}

export async function getTopWords(category: Category, n = 20): Promise<TopWord[]> {
  if (USE_MOCK) return mock.getTopWords(category, n)
  const { data } = await apiClient.get<TopWord[]>('/model/top-words', {
    params: { class: category, n },
  })
  return data
}
