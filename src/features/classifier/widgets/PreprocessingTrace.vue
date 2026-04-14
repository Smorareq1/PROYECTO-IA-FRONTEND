<script setup lang="ts">
import { ref } from 'vue'
import { ChevronDown, ChevronRight } from 'lucide-vue-next'
import type { Prediction } from '../models/prediction'
import { CATEGORY_LABELS } from '@/core/config/constants'
import { formatPercent } from '@/core/utils/format'

const props = defineProps<{ prediction: Prediction }>()

const open = ref(false)

const logProbEntries = Object.entries(props.prediction.log_probs)
  .sort(([, a], [, b]) => b - a)
</script>

<template>
  <div class="trace">
    <button class="trace__toggle" @click="open = !open">
      <component :is="open ? ChevronDown : ChevronRight" :size="15" />
      <span>Detalle técnico del preprocesamiento</span>
    </button>

    <div v-if="open" class="trace__body">
      <!-- Tokens -->
      <div class="trace__section">
        <p class="trace__section-label">Tokens extraídos ({{ prediction.tokens.length }})</p>
        <div class="trace__tokens">
          <span v-for="token in prediction.tokens" :key="token" class="trace__token">
            {{ token }}
          </span>
        </div>
      </div>

      <!-- Log-probs -->
      <div class="trace__section">
        <p class="trace__section-label">Log-probabilidades por clase</p>
        <div class="trace__logprobs">
          <div
            v-for="[cat, lp] in logProbEntries"
            :key="cat"
            class="trace__logprob-row"
            :class="{ 'trace__logprob-row--highlight': cat === prediction.category }"
          >
            <span class="trace__logprob-cat">{{ CATEGORY_LABELS[cat as keyof typeof CATEGORY_LABELS] }}</span>
            <span class="trace__logprob-val">{{ lp.toFixed(4) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trace {
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  overflow: hidden;
}

.trace__toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px 16px;
  background: var(--ds-neutral-50);
  border: none;
  color: var(--ds-text-secondary);
  font-size: var(--ds-text-sm);
  font-weight: 500;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}

.trace__toggle:hover { background: var(--ds-neutral-100); }

:global(.dark .trace__toggle) { background: #18181B; }
:global(.dark .trace__toggle:hover) { background: #27272A; }

.trace__body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  border-top: 1px solid var(--ds-border);
}

.trace__section-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 10px;
}

.trace__tokens { display: flex; flex-wrap: wrap; gap: 5px; }

.trace__token {
  display: inline-block;
  padding: 2px 8px;
  background: var(--ds-neutral-100);
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-mono);
  color: var(--ds-text-secondary);
}

:global(.dark .trace__token) { background: #27272A; }

.trace__logprobs { display: flex; flex-direction: column; gap: 4px; }

.trace__logprob-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 10px;
  border-radius: var(--ds-radius-sm);
  background: var(--ds-neutral-50);
  font-size: var(--ds-text-xs);
}

:global(.dark .trace__logprob-row) { background: #18181B; }

.trace__logprob-row--highlight {
  background: rgba(15, 98, 254, 0.06);
  font-weight: 600;
}

.trace__logprob-cat { color: var(--ds-text-primary); }

.trace__logprob-val {
  font-family: var(--ds-font-mono);
  color: var(--ds-text-muted);
}
</style>
