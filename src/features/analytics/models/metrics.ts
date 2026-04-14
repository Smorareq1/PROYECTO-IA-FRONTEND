import type { Category } from '@/core/config/constants'

export interface ClassMetrics {
  class: Category
  precision: number
  recall: number
  f1: number
  support: number
}

export interface ModelMetrics {
  accuracy: number
  macro_f1: number
  per_class: ClassMetrics[]
}

export interface ConfusionMatrix {
  labels: Category[]
  matrix: number[][]
}

export interface ModelInfo {
  version: string
  trained_at: string
  vocab_size: number
  doc_count: number
  classes: Category[]
}

export interface TopWord {
  word: string
  weight: number
}
