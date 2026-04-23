<script setup lang="ts">
import { ref, watch } from 'vue'
import { X, User, Clock, Tag, Trash2 } from 'lucide-vue-next'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import type { Ticket } from '../models/ticket'
import { getTicket } from '../services/tickets.service'
import TicketStatusBadge from './TicketStatusBadge.vue'
import CategoryBadge from '@/design-system/atoms/CategoryBadge.vue'
import ConfidenceBar from '@/design-system/molecules/ConfidenceBar.vue'
import CategoryReassignDialog from './CategoryReassignDialog.vue'
import { TICKET_STATUSES, STATUS_LABELS } from '@/core/config/constants'
import { useTicketMutations } from '../composables/useTicketMutations'

const props = defineProps<{ ticket: Ticket }>()
const emit = defineEmits<{ close: []; deleted: [] }>()

const { update, remove, isSubmitting } = useTicketMutations()
const showReassign = ref(false)

// Local reactive copy so the card updates after mutations
const local = ref<Ticket>({ ...props.ticket })

// Sync if parent changes the ticket prop
watch(() => props.ticket, (t) => { local.value = { ...t } })

const effectiveCategory = () =>
  local.value.final_category ?? local.value.predicted_category

function formatDate(iso: string) {
  return format(new Date(iso), "d 'de' MMMM yyyy, HH:mm", { locale: es })
}

async function refreshLocal() {
  try {
    const fresh = await getTicket(local.value.id)
    local.value = fresh
  } catch {
    // ticket may have been deleted
  }
}

async function changeStatus(status: string) {
  await update(local.value.id, { status: status as Ticket['status'] })
  await refreshLocal()
}

async function onCategorySaved() {
  showReassign.value = false
  await refreshLocal()
}

async function handleDelete() {
  await remove(local.value.id)
  emit('deleted')
  emit('close')
}
</script>

<template>
  <div class="panel-overlay" @click.self="emit('close')">
    <div class="panel">
      <!-- Header -->
      <div class="panel__header">
        <div>
          <p class="panel__id">{{ local.id }}</p>
          <h2 class="panel__title">{{ local.subject }}</h2>
        </div>
        <button class="panel__close" @click="emit('close')">
          <X :size="20" />
        </button>
      </div>

      <!-- Meta row -->
      <div class="panel__meta">
        <TicketStatusBadge :status="local.status" />
        <CategoryBadge :category="effectiveCategory()" />
        <span v-if="local.final_category" class="panel__corrected-tag">Categoría corregida</span>
      </div>

      <!-- Description -->
      <div class="panel__section">
        <p class="panel__section-label">Descripción</p>
        <p class="panel__description">{{ local.description }}</p>
      </div>

      <!-- AI Prediction -->
      <div class="panel__section">
        <p class="panel__section-label">Confianza del modelo</p>
        <ConfidenceBar
          :confidences="local.confidences"
          :highlight-category="local.predicted_category"
          :animated="false"
        />
      </div>

      <!-- Info -->
      <div class="panel__info">
        <div class="panel__info-item">
          <User :size="13" />
          <span>{{ local.created_by }}</span>
        </div>
        <div class="panel__info-item">
          <Clock :size="13" />
          <span>{{ formatDate(local.created_at) }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="panel__actions">
        <select
          class="panel__select"
          :value="local.status"
          :disabled="isSubmitting"
          @change="changeStatus(($event.target as HTMLSelectElement).value)"
        >
          <option v-for="st in TICKET_STATUSES" :key="st" :value="st">
            {{ STATUS_LABELS[st] }}
          </option>
        </select>

        <button class="panel__btn panel__btn--secondary" @click="showReassign = true">
          <Tag :size="14" />
          Reasignar categoría
        </button>

        <button class="panel__btn panel__btn--danger" :disabled="isSubmitting" @click="handleDelete">
          <Trash2 :size="14" />
          Eliminar
        </button>
      </div>
    </div>
  </div>

  <CategoryReassignDialog
    v-if="showReassign"
    :ticket="local"
    @close="showReassign = false"
    @saved="onCategorySaved"
  />
</template>

<style scoped>
.panel-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.panel {
  width: 480px;
  max-width: 100%;
  max-height: calc(100vh - 120px);
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: popIn 0.2s ease-out;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2), 0 0 0 1px rgba(0, 0, 0, 0.05);
}

@keyframes popIn {
  from { opacity: 0; transform: scale(0.96) translateY(8px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

:global(.dark .panel) {
  background: #09090B;
  border-color: #27272A;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.panel__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.panel__id {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin-bottom: 4px;
}

.panel__title {
  font-size: var(--ds-text-lg);
  font-weight: 600;
  color: var(--ds-text-primary);
  line-height: 1.3;
}

.panel__close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: none;
  color: var(--ds-text-muted);
  cursor: pointer;
  transition: all 0.15s;
}

.panel__close:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
}

.panel__meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.panel__corrected-tag {
  font-size: 0.625rem;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: var(--ds-radius-sm);
  background: rgba(241, 194, 27, 0.15);
  color: var(--ds-warning);
}

.panel__section-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 10px;
}

.panel__description {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  line-height: 1.6;
  white-space: pre-wrap;
}

.panel__info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 4px;
  border-top: 1px solid var(--ds-border);
}

.panel__info-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.panel__actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid var(--ds-border);
}

.panel__select {
  height: 36px;
  padding: 0 10px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-sm);
  font-family: var(--ds-font-sans);
  cursor: pointer;
}

.panel__btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 0 14px;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.panel__btn--secondary {
  border: 1px solid var(--ds-border);
  background: none;
  color: var(--ds-text-secondary);
}

.panel__btn--secondary:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
}

.panel__btn--danger {
  border: 1px solid var(--ds-border);
  background: none;
  color: var(--ds-text-muted);
  margin-left: auto;
}

.panel__btn--danger:hover {
  border-color: var(--ds-danger);
  color: var(--ds-danger);
  background: rgba(218, 30, 40, 0.06);
}

.panel__btn--danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
