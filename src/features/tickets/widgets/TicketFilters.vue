<script setup lang="ts">
import { Search, X } from 'lucide-vue-next'
import { CATEGORIES, CATEGORY_LABELS, TICKET_STATUSES, STATUS_LABELS } from '@/core/config/constants'
import { useTicketFilters } from '../composables/useTicketFilters'

const { filters, setFilter, resetFilters } = useTicketFilters()

function onSearch(e: Event) {
  setFilter('q', (e.target as HTMLInputElement).value || undefined)
}

function hasActiveFilters() {
  return !!(filters.value.q || filters.value.status || filters.value.category)
}
</script>

<template>
  <div class="ticket-filters">
    <div class="ticket-filters__search">
      <Search :size="15" class="ticket-filters__search-icon" />
      <input
        class="ticket-filters__input"
        type="text"
        placeholder="Buscar por asunto o descripción…"
        :value="filters.q ?? ''"
        @input="onSearch"
      />
    </div>

    <select
      class="ticket-filters__select"
      :value="filters.category ?? ''"
      @change="setFilter('category', ($event.target as HTMLSelectElement).value || undefined)"
    >
      <option value="">Todas las categorías</option>
      <option v-for="cat in CATEGORIES" :key="cat" :value="cat">
        {{ CATEGORY_LABELS[cat] }}
      </option>
    </select>

    <select
      class="ticket-filters__select"
      :value="filters.status ?? ''"
      @change="setFilter('status', ($event.target as HTMLSelectElement).value || undefined)"
    >
      <option value="">Todos los estados</option>
      <option v-for="st in TICKET_STATUSES" :key="st" :value="st">
        {{ STATUS_LABELS[st] }}
      </option>
    </select>

    <button v-if="hasActiveFilters()" class="ticket-filters__clear" @click="resetFilters">
      <X :size="14" />
      Limpiar
    </button>
  </div>
</template>

<style scoped>
.ticket-filters {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.ticket-filters__search {
  position: relative;
  flex: 1;
  min-width: 200px;
}

.ticket-filters__search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ds-text-muted);
  pointer-events: none;
}

.ticket-filters__input {
  width: 100%;
  height: 36px;
  padding: 0 12px 0 34px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-sm);
  font-family: var(--ds-font-sans);
  outline: none;
  transition: border-color 0.2s;
}

.ticket-filters__input:focus {
  border-color: var(--ds-primary-500);
}

.ticket-filters__select {
  height: 36px;
  padding: 0 10px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-sm);
  font-family: var(--ds-font-sans);
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s;
}

.ticket-filters__select:focus {
  border-color: var(--ds-primary-500);
}

.ticket-filters__clear {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: none;
  color: var(--ds-text-secondary);
  font-size: var(--ds-text-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.ticket-filters__clear:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
}
</style>
