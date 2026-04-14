<script setup lang="ts">
import { ref, computed } from 'vue'
import { ChevronDown, ChevronUp } from 'lucide-vue-next'
import type { ClassMetrics } from '../models/metrics'
import { CATEGORY_LABELS } from '@/core/config/constants'

const props = defineProps<{ metrics: ClassMetrics[] }>()

type SortKey = 'class' | 'precision' | 'recall' | 'f1' | 'support'
const sortKey = ref<SortKey>('f1')
const sortAsc = ref(false)

function toggle(key: SortKey) {
  if (sortKey.value === key) { sortAsc.value = !sortAsc.value }
  else { sortKey.value = key; sortAsc.value = false }
}

const sorted = computed(() => {
  return [...props.metrics].sort((a, b) => {
    const av = sortKey.value === 'class' ? a.class : a[sortKey.value]
    const bv = sortKey.value === 'class' ? b.class : b[sortKey.value]
    const cmp = av < bv ? -1 : av > bv ? 1 : 0
    return sortAsc.value ? cmp : -cmp
  })
})

function pct(v: number) { return `${(v * 100).toFixed(1)}%` }
</script>

<template>
  <div class="per-class">
    <table class="per-class__table">
      <thead>
        <tr>
          <th v-for="col in (['class', 'precision', 'recall', 'f1', 'support'] as SortKey[])" :key="col"
              class="per-class__th"
              @click="toggle(col)"
          >
            {{ { class: 'Clase', precision: 'Precision', recall: 'Recall', f1: 'F1', support: 'Soporte' }[col] }}
            <component
              :is="sortKey === col ? (sortAsc ? ChevronUp : ChevronDown) : ChevronDown"
              :size="12"
              class="per-class__sort-icon"
              :class="{ 'per-class__sort-icon--active': sortKey === col }"
            />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in sorted" :key="row.class" class="per-class__row">
          <td>
            <span class="per-class__cat" :class="`per-class__cat--${row.class}`">
              {{ CATEGORY_LABELS[row.class] }}
            </span>
          </td>
          <td class="per-class__metric">{{ pct(row.precision) }}</td>
          <td class="per-class__metric">{{ pct(row.recall) }}</td>
          <td class="per-class__metric per-class__metric--bold">{{ pct(row.f1) }}</td>
          <td class="per-class__metric per-class__metric--mono">{{ row.support }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.per-class {
  overflow-x: auto;
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
}

:global(.dark .per-class) { background: #18181B; border-color: #27272A; }

.per-class__table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--ds-text-sm);
}

.per-class__th {
  text-align: left;
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  padding: 12px 16px;
  border-bottom: 1px solid var(--ds-border);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
}

.per-class__th:hover { color: var(--ds-text-primary); }

.per-class__sort-icon {
  display: inline;
  margin-left: 4px;
  opacity: 0.3;
  vertical-align: middle;
}

.per-class__sort-icon--active { opacity: 1; }

.per-class__row { transition: background 0.1s; }
.per-class__row:hover { background: var(--ds-neutral-50); }
:global(.dark .per-class__row:hover) { background: #27272A; }

.per-class__row td {
  padding: 11px 16px;
  border-bottom: 1px solid var(--ds-border);
  color: var(--ds-text-primary);
}

.per-class__row:last-child td { border-bottom: none; }

.per-class__cat {
  display: inline-block;
  padding: 2px 9px;
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-weight: 600;
}

.per-class__cat--soporte_tecnico  { color: var(--ds-cat-soporte);    background: var(--ds-cat-soporte-bg); }
.per-class__cat--facturacion      { color: var(--ds-cat-facturacion); background: var(--ds-cat-facturacion-bg); }
.per-class__cat--consulta_general { color: var(--ds-cat-consulta);    background: var(--ds-cat-consulta-bg); }
.per-class__cat--queja            { color: var(--ds-cat-queja);       background: var(--ds-cat-queja-bg); }
.per-class__cat--cancelacion      { color: var(--ds-cat-cancelacion); background: var(--ds-cat-cancelacion-bg); }

.per-class__metric { color: var(--ds-text-secondary); }
.per-class__metric--bold { font-weight: 600; color: var(--ds-text-primary); }
.per-class__metric--mono { font-family: var(--ds-font-mono); }
</style>
