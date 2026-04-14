<script setup lang="ts">
import { computed } from 'vue'
import { Timer } from 'lucide-vue-next'
import type { Prediction } from '../models/prediction'
import { CATEGORY_LABELS } from '@/core/config/constants'
import CategoryBadge from '@/design-system/atoms/CategoryBadge.vue'
import ConfidenceBar from '@/design-system/molecules/ConfidenceBar.vue'

const props = defineProps<{ prediction: Prediction }>()

const topConfidence = computed(() =>
  Math.round(props.prediction.confidences[props.prediction.category] * 100),
)
</script>

<template>
  <div class="pred-card">
    <div class="pred-card__top">
      <div class="pred-card__result">
        <p class="pred-card__result-label">Categoría predicha</p>
        <div class="pred-card__result-row">
          <CategoryBadge :category="prediction.category" size="lg" />
          <span class="pred-card__confidence">{{ topConfidence }}% confianza</span>
        </div>
      </div>
      <div class="pred-card__timing">
        <Timer :size="13" />
        <span>{{ prediction.processing_ms.toFixed(1) }} ms</span>
      </div>
    </div>

    <div class="pred-card__bars">
      <p class="pred-card__section-label">Distribución de confianza</p>
      <ConfidenceBar
        :confidences="prediction.confidences"
        :highlight-category="prediction.category"
      />
    </div>
  </div>
</template>

<style scoped>
.pred-card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeUp 0.25s ease-out;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

:global(.dark .pred-card) { background: #18181B; border-color: #27272A; }

.pred-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.pred-card__result-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 10px;
}

.pred-card__result-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pred-card__confidence {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  font-family: var(--ds-font-mono);
  color: var(--ds-text-secondary);
}

.pred-card__timing {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-mono);
  color: var(--ds-text-muted);
  flex-shrink: 0;
  padding: 4px 10px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-full);
}

.pred-card__section-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 12px;
}
</style>
