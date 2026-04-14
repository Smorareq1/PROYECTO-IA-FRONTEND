import { delay } from '@/mockupdata'
import {
  MOCK_MODEL_INFO,
  MOCK_METRICS,
  MOCK_CONFUSION_MATRIX,
  MOCK_KFOLDS,
  MOCK_TOP_WORDS,
} from '@/mockupdata/data/analytics.data'
import type { ModelInfo, ModelMetrics, ConfusionMatrix, TopWord } from '@/features/analytics/models/metrics'
import type { KFoldReport } from '@/features/analytics/models/kfold'
import type { Category } from '@/core/config/constants'

export async function getModelInfo(): Promise<ModelInfo> {
  await delay(300)
  return structuredClone(MOCK_MODEL_INFO)
}

export async function getMetrics(): Promise<ModelMetrics> {
  await delay(300)
  return structuredClone(MOCK_METRICS)
}

export async function getConfusionMatrix(): Promise<ConfusionMatrix> {
  await delay(300)
  return structuredClone(MOCK_CONFUSION_MATRIX)
}

export async function getKFolds(): Promise<KFoldReport> {
  await delay(300)
  return structuredClone(MOCK_KFOLDS)
}

export async function getTopWords(category: Category, n = 20): Promise<TopWord[]> {
  await delay(200)
  return structuredClone(MOCK_TOP_WORDS[category].slice(0, n))
}
