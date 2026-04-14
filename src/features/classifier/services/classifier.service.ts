import { apiClient } from '@/core/api/client'
import type { Prediction } from '../models/prediction'
import { USE_MOCK } from '@/mockupdata'
import * as mock from '@/mockupdata/services/classifier.mock'

export async function predict(text: string): Promise<Prediction> {
  if (USE_MOCK) return mock.predict(text)
  const { data } = await apiClient.post<Prediction>('/classifier/predict', { text })
  return data
}
