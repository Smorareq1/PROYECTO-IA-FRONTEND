<script setup lang="ts">
import { computed, ref } from 'vue'
import { Timer, TicketPlus, Check, Loader2 } from 'lucide-vue-next'
import type { Prediction } from '../models/prediction'
import { CATEGORY_LABELS } from '@/core/config/constants'
import CategoryBadge from '@/design-system/atoms/CategoryBadge.vue'
import ConfidenceBar from '@/design-system/molecules/ConfidenceBar.vue'
import { createTicket } from '@/features/tickets/services/tickets.service'

const props = defineProps<{ prediction: Prediction; text?: string }>()

const topConfidence = computed(() =>
  Math.round(props.prediction.confidences[props.prediction.category] * 100),
)

const isSaving = ref(false)
const isSaved = ref(false)

async function saveAsTicket() {
  if (isSaving.value || isSaved.value || !props.text) return
  isSaving.value = true
  try {
    const subject = props.text.length > 100 ? props.text.slice(0, 100) + '…' : props.text
    await createTicket({ subject, description: props.text })
    isSaved.value = true
  } catch {
    // Silently fail — user will see the button didn't change state
  } finally {
    isSaving.value = false
  }
}
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

    <div v-if="text" class="pred-card__actions">
      <button
        class="pred-card__save-btn"
        :class="{ 'pred-card__save-btn--saved': isSaved }"
        :disabled="isSaving || isSaved"
        @click="saveAsTicket"
      >
        <Loader2 v-if="isSaving" :size="15" class="pred-card__spin" />
        <Check v-else-if="isSaved" :size="15" />
        <TicketPlus v-else :size="15" />
        <span>{{ isSaved ? 'Ticket creado' : isSaving ? 'Guardando…' : 'Guardar como ticket' }}</span>
      </button>
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

.pred-card__actions {
  border-top: 1px solid var(--ds-border);
  padding-top: 16px;
  display: flex;
  justify-content: flex-end;
}

:global(.dark .pred-card__actions) { border-top-color: #27272A; }

.pred-card__save-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 36px;
  padding: 0 16px;
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: border-color 0.2s ease, background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

:global(.dark .pred-card__save-btn) { background: #18181B; border-color: #27272A; }

.pred-card__save-btn:hover:not(:disabled) {
  border-color: var(--ds-primary-500);
  box-shadow: 0 2px 0 var(--ds-primary-500);
  transform: translateY(-1px);
}

.pred-card__save-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: none;
}

.pred-card__save-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.pred-card__save-btn--saved {
  border-color: var(--ds-cat-feedback);
  color: var(--ds-cat-feedback);
  opacity: 1 !important;
}

.pred-card__spin { animation: predSpin 0.8s linear infinite; }
@keyframes predSpin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
  .pred-card__spin { animation: none; }
}
</style>
