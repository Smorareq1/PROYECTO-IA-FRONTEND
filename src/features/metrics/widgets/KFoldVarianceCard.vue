<script setup lang="ts">
import type { KFoldReport } from '../models/kfold'

const props = defineProps<{ data: KFoldReport }>()

function pct(v: number) { return `${(v * 100).toFixed(2)}%` }
function std(v: number) { return `±${(v * 100).toFixed(2)}%` }
</script>

<template>
  <div class="variance-card">
    <p class="variance-card__title">Resumen K-Fold (k={{ data.k }})</p>

    <div class="variance-card__row">
      <div class="variance-card__metric">
        <span class="variance-card__label">Accuracy media</span>
        <span class="variance-card__value">{{ pct(data.mean.accuracy) }}</span>
        <span class="variance-card__std">{{ std(data.std.accuracy) }}</span>
      </div>
      <div class="variance-card__metric">
        <span class="variance-card__label">Macro F1 media</span>
        <span class="variance-card__value">{{ pct(data.mean.macro_f1) }}</span>
        <span class="variance-card__std">{{ std(data.std.macro_f1) }}</span>
      </div>
    </div>

    <p class="variance-card__footnote">
      La desviación estándar mide la varianza entre folds: valores bajos indican estabilidad del modelo.
    </p>
  </div>
</template>

<style scoped>
.variance-card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 20px;
}

:global(.dark .variance-card) { background: #18181B; border-color: #27272A; }

.variance-card__title {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
  margin-bottom: 16px;
}

.variance-card__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.variance-card__metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: var(--ds-neutral-50);
  border-radius: var(--ds-radius-md);
}

:global(.dark .variance-card__metric) { background: #27272A; }

.variance-card__label {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.variance-card__value {
  font-size: var(--ds-text-xl);
  font-weight: 700;
  font-family: var(--ds-font-mono);
  color: var(--ds-text-primary);
}

.variance-card__std {
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-mono);
  color: var(--ds-text-secondary);
}

.variance-card__footnote {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin-top: 14px;
  line-height: 1.5;
}
</style>
