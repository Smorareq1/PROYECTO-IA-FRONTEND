<script setup lang="ts">
import { ref } from 'vue'
import { X } from 'lucide-vue-next'
import type { Ticket } from '../models/ticket'
import type { Category } from '@/core/config/constants'
import { CATEGORIES, CATEGORY_LABELS } from '@/core/config/constants'
import { useTicketMutations } from '../composables/useTicketMutations'

const props = defineProps<{ ticket: Ticket }>()
const emit = defineEmits<{ close: []; saved: [] }>()

const { update, isSubmitting } = useTicketMutations()
const selected = ref<Category>(props.ticket.final_category ?? props.ticket.predicted_category)

async function save() {
  await update(props.ticket.id, { final_category: selected.value })
  emit('saved')
}
</script>

<template>
  <div class="dialog-overlay" @click.self="emit('close')">
    <div class="dialog">
      <div class="dialog__header">
        <h3 class="dialog__title">Reasignar categoría</h3>
        <button class="dialog__close" @click="emit('close')">
          <X :size="18" />
        </button>
      </div>

      <p class="dialog__hint">
        Categoría predicha por el modelo:
        <strong>{{ CATEGORY_LABELS[ticket.predicted_category] }}</strong>
      </p>

      <div class="dialog__options">
        <label
          v-for="cat in CATEGORIES"
          :key="cat"
          class="dialog__option"
          :class="{ 'dialog__option--selected': selected === cat }"
        >
          <input type="radio" :value="cat" v-model="selected" class="dialog__radio" />
          {{ CATEGORY_LABELS[cat] }}
        </label>
      </div>

      <div class="dialog__footer">
        <button class="dialog__btn dialog__btn--ghost" @click="emit('close')">Cancelar</button>
        <button
          class="dialog__btn dialog__btn--primary"
          :disabled="isSubmitting"
          @click="save"
        >
          {{ isSubmitting ? 'Guardando…' : 'Guardar' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.dialog {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-xl);
  padding: 24px;
  width: 100%;
  max-width: 420px;
  box-shadow: var(--ds-shadow-xl);
  animation: scaleIn 0.18s ease-out;
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}

:global(.dark .dialog) {
  background: #18181B;
  border-color: #3F3F46;
}

.dialog__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.dialog__title {
  font-size: var(--ds-text-base);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.dialog__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  color: var(--ds-text-muted);
  cursor: pointer;
  border-radius: var(--ds-radius-sm);
  transition: all 0.15s;
}

.dialog__close:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
}

.dialog__hint {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  margin-bottom: 16px;
}

.dialog__options {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 20px;
}

.dialog__option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.dialog__option:hover {
  border-color: var(--ds-primary-500);
  background: rgba(15, 98, 254, 0.04);
}

.dialog__option--selected {
  border-color: var(--ds-primary-500);
  background: rgba(15, 98, 254, 0.06);
  color: var(--ds-primary-500);
  font-weight: 500;
}

.dialog__radio {
  accent-color: var(--ds-primary-500);
}

.dialog__footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.dialog__btn {
  display: inline-flex;
  align-items: center;
  height: 36px;
  padding: 0 16px;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 500;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: all 0.15s;
}

.dialog__btn--ghost {
  border: 1px solid var(--ds-border);
  background: none;
  color: var(--ds-text-secondary);
}

.dialog__btn--ghost:hover {
  background: var(--ds-neutral-100);
}

.dialog__btn--primary {
  border: none;
  background: var(--ds-primary-500);
  color: #fff;
}

.dialog__btn--primary:hover:not(:disabled) {
  background: var(--ds-primary-700);
}

.dialog__btn--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
