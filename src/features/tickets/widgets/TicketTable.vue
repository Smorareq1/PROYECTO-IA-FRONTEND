<script setup lang="ts">
import { formatDistanceToNow } from 'date-fns'
import { es } from 'date-fns/locale'
import type { Ticket } from '../models/ticket'
import TicketStatusBadge from './TicketStatusBadge.vue'
import CategoryBadge from '@/design-system/atoms/CategoryBadge.vue'
import EmptyState from '@/design-system/molecules/EmptyState.vue'

defineProps<{
  tickets: Ticket[]
  isLoading?: boolean
}>()

const emit = defineEmits<{
  select: [ticket: Ticket]
}>()

function relativeDate(iso: string) {
  return formatDistanceToNow(new Date(iso), { addSuffix: true, locale: es })
}
</script>

<template>
  <div class="ticket-table-wrap">
    <!-- Skeleton -->
    <div v-if="isLoading" class="ticket-table-skeleton">
      <div v-for="i in 5" :key="i" class="skeleton skeleton-row" />
    </div>

    <!-- Empty -->
    <EmptyState v-else-if="!tickets.length" title="Sin tickets" message="No se encontraron tickets con los filtros aplicados." />

    <!-- Table -->
    <table v-else class="ticket-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Asunto</th>
          <th>Categoría</th>
          <th>Estado</th>
          <th>Creado</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="ticket in tickets"
          :key="ticket.id"
          class="ticket-table__row"
          @click="emit('select', ticket)"
        >
          <td class="ticket-table__id">{{ ticket.id }}</td>
          <td class="ticket-table__subject">
            <span class="ticket-table__subject-text">{{ ticket.subject }}</span>
            <span v-if="ticket.final_category && ticket.final_category !== ticket.predicted_category" class="ticket-table__corrected">corregido</span>
          </td>
          <td>
            <CategoryBadge :category="ticket.final_category ?? ticket.predicted_category" size="sm" />
          </td>
          <td>
            <TicketStatusBadge :status="ticket.status" size="sm" />
          </td>
          <td class="ticket-table__date">{{ relativeDate(ticket.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.ticket-table-wrap {
  overflow-x: auto;
}

.ticket-table-skeleton {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-row {
  height: 48px;
  border-radius: var(--ds-radius-md);
}

.ticket-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--ds-text-sm);
}

.ticket-table th {
  text-align: left;
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  padding: 8px 12px;
  border-bottom: 1px solid var(--ds-border);
}

.ticket-table__row {
  cursor: pointer;
  transition: background 0.1s;
}

.ticket-table__row:hover {
  background: var(--ds-neutral-50);
}

:global(.dark .ticket-table__row:hover) {
  background: #18181B;
}

.ticket-table td {
  padding: 12px 12px;
  border-bottom: 1px solid var(--ds-border);
  color: var(--ds-text-primary);
  vertical-align: middle;
}

.ticket-table__id {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted) !important;
  white-space: nowrap;
}

.ticket-table__subject {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ticket-table__subject-text {
  max-width: 360px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ticket-table__corrected {
  font-size: 0.625rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: var(--ds-radius-sm);
  background: rgba(241, 194, 27, 0.15);
  color: var(--ds-warning);
  white-space: nowrap;
}

.ticket-table__date {
  color: var(--ds-text-muted) !important;
  white-space: nowrap;
}
</style>
