<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import { getTicket } from '../services/tickets.service'
import type { Ticket } from '../models/ticket'
import CategoryBadge from '@/design-system/atoms/CategoryBadge.vue'
import TicketStatusBadge from '../widgets/TicketStatusBadge.vue'
import ConfidenceBar from '@/design-system/molecules/ConfidenceBar.vue'

const route = useRoute()
const router = useRouter()
const ticket = ref<Ticket | null>(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    ticket.value = await getTicket(route.params.id as string)
  } finally {
    isLoading.value = false
  }
})

function formatDate(iso: string) {
  return format(new Date(iso), "d 'de' MMMM yyyy 'a las' HH:mm", { locale: es })
}
</script>

<template>
  <div class="ticket-detail">
    <button class="back-btn" @click="router.back()">
      <ArrowLeft :size="16" />
      Volver
    </button>

    <div v-if="isLoading" class="skeleton-wrap">
      <div class="skeleton" style="height: 32px; width: 240px; margin-bottom: 16px;" />
      <div class="skeleton" style="height: 80px;" />
    </div>

    <template v-else-if="ticket">
      <div class="ticket-detail__header">
        <div>
          <p class="ticket-detail__id">{{ ticket.id }}</p>
          <h1 class="ticket-detail__title">{{ ticket.subject }}</h1>
        </div>
        <div class="ticket-detail__badges">
          <TicketStatusBadge :status="ticket.status" />
          <CategoryBadge :category="ticket.final_category ?? ticket.predicted_category" />
        </div>
      </div>

      <div class="ticket-detail__grid">
        <div class="ticket-detail__main">
          <div class="ticket-detail__card">
            <p class="ticket-detail__card-label">Descripción</p>
            <p class="ticket-detail__description">{{ ticket.description }}</p>
          </div>

          <div class="ticket-detail__card">
            <p class="ticket-detail__card-label">Confianza del modelo Naïve Bayes</p>
            <ConfidenceBar
              :confidences="ticket.confidences"
              :highlight-category="ticket.predicted_category"
            />
          </div>
        </div>

        <div class="ticket-detail__sidebar">
          <div class="ticket-detail__card">
            <p class="ticket-detail__card-label">Información</p>
            <dl class="ticket-detail__info">
              <div class="ticket-detail__info-row">
                <dt>Creado por</dt>
                <dd>{{ ticket.created_by }}</dd>
              </div>
              <div class="ticket-detail__info-row">
                <dt>Fecha</dt>
                <dd>{{ formatDate(ticket.created_at) }}</dd>
              </div>
              <div class="ticket-detail__info-row">
                <dt>Categoría IA</dt>
                <dd><CategoryBadge :category="ticket.predicted_category" size="sm" /></dd>
              </div>
              <div v-if="ticket.final_category" class="ticket-detail__info-row">
                <dt>Categoría final</dt>
                <dd><CategoryBadge :category="ticket.final_category" size="sm" /></dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.ticket-detail { max-width: 900px; }

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 12px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: none;
  color: var(--ds-text-secondary);
  font-size: var(--ds-text-sm);
  cursor: pointer;
  margin-bottom: 24px;
  transition: all 0.15s;
}

.back-btn:hover { background: var(--ds-neutral-100); color: var(--ds-text-primary); }

.skeleton-wrap { display: flex; flex-direction: column; gap: 12px; }

.ticket-detail__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.ticket-detail__id {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin-bottom: 4px;
}

.ticket-detail__title {
  font-size: var(--ds-text-2xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.02em;
}

.ticket-detail__badges { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

.ticket-detail__grid {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
}

@media (max-width: 768px) {
  .ticket-detail__grid { grid-template-columns: 1fr; }
}

.ticket-detail__card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 20px;
  margin-bottom: 16px;
}

:global(.dark .ticket-detail__card) { background: #18181B; border-color: #27272A; }

.ticket-detail__card-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 12px;
}

.ticket-detail__description {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  line-height: 1.7;
  white-space: pre-wrap;
}

.ticket-detail__info { display: flex; flex-direction: column; gap: 10px; }

.ticket-detail__info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.ticket-detail__info-row dt {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.ticket-detail__info-row dd {
  font-size: var(--ds-text-xs);
  font-weight: 500;
  color: var(--ds-text-primary);
  text-align: right;
}
</style>
