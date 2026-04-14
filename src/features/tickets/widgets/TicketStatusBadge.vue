<script setup lang="ts">
import type { TicketStatus } from '@/core/config/constants'
import { STATUS_LABELS } from '@/core/config/constants'

const props = withDefaults(defineProps<{
  status: TicketStatus
  size?: 'sm' | 'md'
}>(), { size: 'md' })
</script>

<template>
  <span class="status-badge" :class="[`status-badge--${status}`, `status-badge--${size}`]">
    {{ STATUS_LABELS[status] }}
  </span>
</template>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
  border-radius: var(--ds-radius-sm);
  white-space: nowrap;
}

.status-badge--sm { font-size: 0.6875rem; padding: 2px 8px; }
.status-badge--md { font-size: var(--ds-text-xs); padding: 4px 10px; }

.status-badge--abierto     { color: var(--ds-info);    background: rgba(0, 67, 206, 0.1); }
.status-badge--en_progreso { color: var(--ds-warning);  background: rgba(241, 194, 27, 0.12); }
.status-badge--resuelto    { color: var(--ds-success);  background: rgba(25, 128, 56, 0.1); }
.status-badge--cerrado     { color: var(--ds-text-muted); background: var(--ds-neutral-100); }
</style>
