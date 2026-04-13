<script setup lang="ts">
import { computed } from 'vue'
import type { Category } from '@/core/config/constants'
import { CATEGORY_LABELS } from '@/core/config/constants'
import { formatPercent } from '@/core/utils/format'

interface Props {
  confidences: Record<string, number>
  highlightCategory?: Category
  animated?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  animated: true,
})

const sortedConfidences = computed(() => {
  return Object.entries(props.confidences)
    .sort(([, a], [, b]) => b - a)
    .map(([category, value]) => ({
      category: category as Category,
      value,
      label: CATEGORY_LABELS[category as Category] || category,
      isHighlight: category === props.highlightCategory,
    }))
})
</script>

<template>
  <div class="confidence-bars">
    <div
      v-for="item in sortedConfidences"
      :key="item.category"
      class="confidence-bars__item"
      :class="{ 'confidence-bars__item--highlight': item.isHighlight }"
    >
      <div class="confidence-bars__label">
        <span class="confidence-bars__name">{{ item.label }}</span>
        <span class="confidence-bars__value">{{ formatPercent(item.value) }}</span>
      </div>
      <div class="confidence-bars__track">
        <div
          class="confidence-bars__fill"
          :class="[`confidence-bars__fill--${item.category}`, { 'confidence-bars__fill--animated': animated }]"
          :style="{ '--bar-width': `${item.value * 100}%` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.confidence-bars {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.confidence-bars__item {
  opacity: 0.65;
  transition: opacity 0.2s ease;
}

.confidence-bars__item--highlight {
  opacity: 1;
}

.confidence-bars__item:hover {
  opacity: 1;
}

.confidence-bars__label {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
}

.confidence-bars__name {
  font-size: var(--ds-text-sm);
  font-weight: 500;
  color: var(--ds-text-primary);
}

.confidence-bars__value {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  font-family: var(--ds-font-mono);
  color: var(--ds-text-secondary);
}

.confidence-bars__track {
  height: 8px;
  background: var(--ds-neutral-100);
  border-radius: var(--ds-radius-full);
  overflow: hidden;
}

.confidence-bars__fill {
  height: 100%;
  border-radius: var(--ds-radius-full);
  width: var(--bar-width);
  transition: width 0.3s ease;
}

.confidence-bars__fill--animated {
  animation: barFill 0.8s ease-out forwards;
  width: 0;
}

@keyframes barFill {
  from { width: 0; }
  to { width: var(--bar-width); }
}

/* Category fill colors */
.confidence-bars__fill--soporte_tecnico  { background: var(--ds-cat-soporte); }
.confidence-bars__fill--facturacion      { background: var(--ds-cat-facturacion); }
.confidence-bars__fill--consulta_general { background: var(--ds-cat-consulta); }
.confidence-bars__fill--queja           { background: var(--ds-cat-queja); }
.confidence-bars__fill--cancelacion     { background: var(--ds-cat-cancelacion); }
</style>
