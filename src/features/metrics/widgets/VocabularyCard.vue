<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Category } from '@/core/config/constants'
import { CATEGORIES, CATEGORY_LABELS } from '@/core/config/constants'
import type { TopWord } from '../models/metrics'
import { getTopWords } from '../services/metrics.service'
import { handleError } from '@/core/errors/handler'

const selected = ref<Category>('soporte_tecnico')
const words = ref<TopWord[]>([])
const isLoading = ref(false)

const maxWeight = ref(1)

async function loadWords(cat: Category) {
  isLoading.value = true
  try {
    words.value = await getTopWords(cat, 15)
    maxWeight.value = Math.max(...words.value.map(w => w.weight), 1)
  } catch (e) {
    handleError(e)
  } finally {
    isLoading.value = false
  }
}

watch(selected, loadWords, { immediate: true })
</script>

<template>
  <div class="vocab-card">
    <div class="vocab-card__header">
      <p class="vocab-card__title">Top palabras por categoría</p>
      <select v-model="selected" class="vocab-card__select">
        <option v-for="cat in CATEGORIES" :key="cat" :value="cat">
          {{ CATEGORY_LABELS[cat] }}
        </option>
      </select>
    </div>

    <div v-if="isLoading" class="vocab-card__skeleton">
      <div v-for="i in 8" :key="i" class="skeleton" :style="{ height: '28px', width: `${40 + i * 7}%` }" />
    </div>

    <div v-else class="vocab-card__words">
      <div v-for="word in words" :key="word.word" class="vocab-card__word">
        <span class="vocab-card__word-text">{{ word.word }}</span>
        <div class="vocab-card__word-bar">
          <div
            class="vocab-card__word-fill"
            :class="`vocab-card__word-fill--${selected}`"
            :style="{ width: `${(word.weight / maxWeight) * 100}%` }"
          />
        </div>
        <span class="vocab-card__word-val">{{ word.weight.toFixed(3) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vocab-card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 20px;
}

:global(.dark .vocab-card) { background: #18181B; border-color: #27272A; }

.vocab-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.vocab-card__title {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.vocab-card__select {
  height: 30px;
  padding: 0 8px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-sans);
  cursor: pointer;
}

.vocab-card__skeleton { display: flex; flex-direction: column; gap: 6px; }

.vocab-card__words { display: flex; flex-direction: column; gap: 6px; }

.vocab-card__word {
  display: grid;
  grid-template-columns: 130px 1fr 60px;
  align-items: center;
  gap: 10px;
}

.vocab-card__word-text {
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-mono);
  color: var(--ds-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vocab-card__word-bar {
  height: 6px;
  background: var(--ds-neutral-100);
  border-radius: var(--ds-radius-full);
  overflow: hidden;
}

:global(.dark .vocab-card__word-bar) { background: #27272A; }

.vocab-card__word-fill {
  height: 100%;
  border-radius: var(--ds-radius-full);
  transition: width 0.4s ease;
}

.vocab-card__word-fill--soporte_tecnico  { background: var(--ds-cat-soporte); }
.vocab-card__word-fill--facturacion      { background: var(--ds-cat-facturacion); }
.vocab-card__word-fill--consulta_general { background: var(--ds-cat-consulta); }
.vocab-card__word-fill--queja            { background: var(--ds-cat-queja); }
.vocab-card__word-fill--cancelacion      { background: var(--ds-cat-cancelacion); }

.vocab-card__word-val {
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-mono);
  color: var(--ds-text-muted);
  text-align: right;
}
</style>
