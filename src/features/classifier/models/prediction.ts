import type { Category } from '@/core/config/constants'

export interface Prediction {
  category: Category
  confidences: Record<Category, number>
  log_probs: Record<Category, number>
  tokens: string[]
  processing_ms: number
}
