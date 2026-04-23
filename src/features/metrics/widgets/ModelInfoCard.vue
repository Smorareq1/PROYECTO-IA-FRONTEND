<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import { Brain, Calendar, BookOpen, Layers } from 'lucide-vue-next'
import type { ModelInfo } from '../models/metrics'
import { CATEGORY_LABELS } from '@/core/config/constants'

const props = defineProps<{ info: ModelInfo }>()

const trainedAt = computed(() =>
  format(new Date(props.info.trained_at), "d 'de' MMMM yyyy, HH:mm", { locale: es }),
)
</script>

<template>
  <div class="model-info">
    <div class="model-info__header">
      <div class="model-info__icon">
        <Brain :size="20" />
      </div>
      <div>
        <p class="model-info__name">Naïve Bayes Classifier</p>
        <p class="model-info__version">v{{ info.version }}</p>
      </div>
    </div>

    <div class="model-info__grid">
      <div class="model-info__item">
        <Calendar :size="14" class="model-info__item-icon" />
        <div>
          <p class="model-info__item-label">Entrenado</p>
          <p class="model-info__item-value">{{ trainedAt }}</p>
        </div>
      </div>
      <div class="model-info__item">
        <BookOpen :size="14" class="model-info__item-icon" />
        <div>
          <p class="model-info__item-label">Vocabulario</p>
          <p class="model-info__item-value">{{ info.vocab_size.toLocaleString() }} palabras</p>
        </div>
      </div>
      <div class="model-info__item">
        <Layers :size="14" class="model-info__item-icon" />
        <div>
          <p class="model-info__item-label">Dataset</p>
          <p class="model-info__item-value">{{ info.doc_count.toLocaleString() }} documentos</p>
        </div>
      </div>
    </div>

    <div class="model-info__classes">
      <p class="model-info__classes-label">Clases entrenadas</p>
      <div class="model-info__classes-list">
        <span v-for="cls in info.classes" :key="cls" class="model-info__cls" :class="`model-info__cls--${cls}`">
          {{ CATEGORY_LABELS[cls] }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.model-info {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

:global(.dark .model-info) { background: #18181B; border-color: #27272A; }

.model-info__header { display: flex; align-items: center; gap: 12px; }

.model-info__icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--ds-primary-500), var(--ds-primary-700));
  border-radius: var(--ds-radius-lg);
  color: #fff;
  flex-shrink: 0;
}

.model-info__name {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.model-info__version {
  font-size: var(--ds-text-xs);
  font-family: var(--ds-font-mono);
  color: var(--ds-text-muted);
}

.model-info__grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 4px;
  border-top: 1px solid var(--ds-border);
}

.model-info__item { display: flex; align-items: flex-start; gap: 10px; }

.model-info__item-icon { color: var(--ds-text-muted); margin-top: 2px; flex-shrink: 0; }

.model-info__item-label {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.model-info__item-value {
  font-size: var(--ds-text-sm);
  font-weight: 500;
  color: var(--ds-text-primary);
}

.model-info__classes-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 8px;
}

.model-info__classes-list { display: flex; flex-wrap: wrap; gap: 6px; }

.model-info__cls {
  display: inline-block;
  padding: 2px 8px;
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-weight: 600;
}

.model-info__cls--ACCOUNT      { color: var(--ds-cat-account);      background: var(--ds-cat-account-bg); }
.model-info__cls--CANCEL       { color: var(--ds-cat-cancel);       background: var(--ds-cat-cancel-bg); }
.model-info__cls--CONTACT      { color: var(--ds-cat-contact);      background: var(--ds-cat-contact-bg); }
.model-info__cls--DELIVERY     { color: var(--ds-cat-delivery);     background: var(--ds-cat-delivery-bg); }
.model-info__cls--FEEDBACK     { color: var(--ds-cat-feedback);     background: var(--ds-cat-feedback-bg); }
.model-info__cls--INVOICE      { color: var(--ds-cat-invoice);      background: var(--ds-cat-invoice-bg); }
.model-info__cls--ORDER        { color: var(--ds-cat-order);        background: var(--ds-cat-order-bg); }
.model-info__cls--PAYMENT      { color: var(--ds-cat-payment);      background: var(--ds-cat-payment-bg); }
.model-info__cls--REFUND       { color: var(--ds-cat-refund);       background: var(--ds-cat-refund-bg); }
.model-info__cls--SHIPPING     { color: var(--ds-cat-shipping);     background: var(--ds-cat-shipping-bg); }
.model-info__cls--SUBSCRIPTION { color: var(--ds-cat-subscription); background: var(--ds-cat-subscription-bg); }
</style>
