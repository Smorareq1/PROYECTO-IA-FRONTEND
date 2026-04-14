import { delay } from '@/mockupdata'
import { MOCK_TOP_WORDS } from '@/mockupdata/data/metrics.data'
import type { Prediction } from '@/features/classifier/models/prediction'
import type { Category } from '@/core/config/constants'
import { CATEGORIES } from '@/core/config/constants'

/**
 * Simple tokeniser: lowercase, strip punctuation, split on whitespace.
 * Mirrors the preprocessing a real Naïve Bayes pipeline would do.
 */
function tokenise(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^\w\sáéíóúüñ]/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
}

/**
 * Score a token list against a category's top-word vocabulary.
 * Returns a pseudo-log-probability (negative, higher = better).
 */
function scoreCategory(tokens: string[], category: Category): number {
  const vocab = MOCK_TOP_WORDS[category]
  const vocabMap = Object.fromEntries(vocab.map(w => [w.word, w.weight]))
  const vocabSize = 4817
  const alpha = 1 // Laplace smoothing

  let logProb = Math.log(1 / CATEGORIES.length) // uniform prior
  for (const token of tokens) {
    const weight = vocabMap[token] ?? 0
    // Convert weight to a pseudo-count; unseen words get a small smoothed value
    const count = weight > 0 ? weight * 10 : alpha
    logProb += Math.log((count + alpha) / (vocabSize + alpha * vocabSize))
  }
  return logProb
}

export async function predict(text: string): Promise<Prediction> {
  const start = Date.now()
  await delay(350)

  const tokens = tokenise(text)

  const rawScores = {} as Record<Category, number>
  for (const cat of CATEGORIES) {
    rawScores[cat] = scoreCategory(tokens, cat)
  }

  // Softmax over log-probs to get confidences
  const maxScore = Math.max(...Object.values(rawScores))
  const exps = {} as Record<Category, number>
  let expSum = 0
  for (const cat of CATEGORIES) {
    exps[cat] = Math.exp(rawScores[cat] - maxScore)
    expSum += exps[cat]
  }

  const confidences = {} as Record<Category, number>
  for (const cat of CATEGORIES) {
    confidences[cat] = parseFloat((exps[cat] / expSum).toFixed(4))
  }

  // Re-normalise to fix floating-point drift
  const sum = Object.values(confidences).reduce((s, v) => s + v, 0)
  const best = CATEGORIES.reduce((a, b) => (confidences[a] > confidences[b] ? a : b))
  confidences[best] = parseFloat((confidences[best] + (1 - sum)).toFixed(4))

  const category = CATEGORIES.reduce((a, b) => (confidences[a] > confidences[b] ? a : b))

  return {
    category,
    confidences,
    log_probs: rawScores,
    tokens,
    processing_ms: Date.now() - start,
  }
}
