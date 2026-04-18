import type { ClassMetrics } from './metrics'

export interface KFoldResult {
  fold: number
  accuracy: number
  macro_f1: number
  per_class: ClassMetrics[]
}

export interface KFoldReport {
  k: number
  folds: KFoldResult[]
  mean: { accuracy: number; macro_f1: number }
  std: { accuracy: number; macro_f1: number }
}
