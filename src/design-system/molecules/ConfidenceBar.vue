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

:global(.dark .confidence-bars__track) {
  background: #27272A;
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

/* Category fill colors (11 Bitext dataset categories) */
.confidence-bars__fill--ACCOUNT      { background: var(--ds-cat-account); }
.confidence-bars__fill--CANCEL       { background: var(--ds-cat-cancel); }
.confidence-bars__fill--CONTACT      { background: var(--ds-cat-contact); }
.confidence-bars__fill--DELIVERY     { background: var(--ds-cat-delivery); }
.confidence-bars__fill--FEEDBACK     { background: var(--ds-cat-feedback); }
.confidence-bars__fill--INVOICE      { background: var(--ds-cat-invoice); }
.confidence-bars__fill--ORDER        { background: var(--ds-cat-order); }
.confidence-bars__fill--PAYMENT      { background: var(--ds-cat-payment); }
.confidence-bars__fill--REFUND       { background: var(--ds-cat-refund); }
.confidence-bars__fill--SHIPPING     { background: var(--ds-cat-shipping); }
.confidence-bars__fill--SUBSCRIPTION { background: var(--ds-cat-subscription); }
</style>
