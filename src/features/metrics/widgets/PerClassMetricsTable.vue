<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ArrowDown, ArrowUp, ArrowDownUp } from 'lucide-vue-next'
import type { ClassMetrics } from '../models/metrics'
import { CATEGORY_LABELS } from '@/core/config/constants'

const props = defineProps<{ metrics: ClassMetrics[] }>()

type SortKey = 'class' | 'precision' | 'recall' | 'f1' | 'support'
const sortKey = ref<SortKey>('f1')
const sortAsc = ref(false)
const animatedIn = ref(false)

onMounted(() => {
  requestAnimationFrame(() => { animatedIn.value = true })
})

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

const maxSupport = computed(() =>
  Math.max(...props.metrics.map(m => m.support), 1),
)

function catColor(cls: string) {
  return `var(--ds-cat-${cls.toLowerCase()})`
}

function pct(v: number) { return `${(v * 100).toFixed(1)}%` }
</script>

<template>
  <div class="per-class">
    <table class="per-class__table">
      <thead>
        <tr>
          <th
            v-for="col in (['class', 'precision', 'recall', 'f1', 'support'] as SortKey[])"
            :key="col"
            class="per-class__th"
            :class="{ 'per-class__th--num': col !== 'class' }"
            @click="toggle(col)"
          >
            <span class="per-class__th-inner">
              {{ { class: 'Clase', precision: 'Precision', recall: 'Recall', f1: 'F1', support: 'Soporte' }[col] }}
              <component
                :is="sortKey === col ? (sortAsc ? ArrowUp : ArrowDown) : ArrowDownUp"
                :size="12"
                class="per-class__sort-icon"
                :class="{ 'per-class__sort-icon--active': sortKey === col }"
              />
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, i) in sorted"
          :key="row.class"
          class="per-class__row"
          :class="{ 'per-class__row--in': animatedIn }"
          :style="{ transitionDelay: `${i * 45}ms` }"
        >
          <td class="per-class__cell-class">
            <span class="per-class__cat" :class="`per-class__cat--${row.class}`">
              <span class="per-class__cat-dot"></span>
              {{ CATEGORY_LABELS[row.class] }}
            </span>
          </td>

          <td class="per-class__metric-cell">
            <div class="per-class__meter">
              <div class="per-class__meter-track">
                <div
                  class="per-class__meter-fill per-class__meter-fill--precision"
                  :style="{ width: animatedIn ? `${row.precision * 100}%` : '0%' }"
                ></div>
              </div>
              <span class="per-class__metric-val">{{ pct(row.precision) }}</span>
            </div>
          </td>

          <td class="per-class__metric-cell">
            <div class="per-class__meter">
              <div class="per-class__meter-track">
                <div
                  class="per-class__meter-fill per-class__meter-fill--recall"
                  :style="{ width: animatedIn ? `${row.recall * 100}%` : '0%' }"
                ></div>
              </div>
              <span class="per-class__metric-val">{{ pct(row.recall) }}</span>
            </div>
          </td>

          <td class="per-class__metric-cell">
            <div class="per-class__meter">
              <div class="per-class__meter-track per-class__meter-track--strong">
                <div
                  class="per-class__meter-fill per-class__meter-fill--f1"
                  :style="{
                    width: animatedIn ? `${row.f1 * 100}%` : '0%',
                    background: catColor(row.class),
                  }"
                ></div>
              </div>
              <span class="per-class__metric-val per-class__metric-val--bold">{{ pct(row.f1) }}</span>
            </div>
          </td>

          <td class="per-class__metric-cell">
            <div class="per-class__support">
              <div class="per-class__support-bar">
                <div
                  class="per-class__support-fill"
                  :style="{ width: animatedIn ? `${(row.support / maxSupport) * 100}%` : '0%' }"
                ></div>
              </div>
              <span class="per-class__support-val">{{ row.support }}</span>
            </div>
          </td>
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
  border-radius: var(--ds-radius-md);
}

:global(.dark .per-class) { background: #18181B; border-color: #27272A; }

.per-class__table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--ds-text-sm);
}

.per-class__th {
  text-align: left;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ds-text-muted);
  padding: 14px 18px;
  border-bottom: 1px solid var(--ds-border);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  background: var(--ds-surface-raised);
  transition: color 0.2s ease;
}

:global(.dark .per-class__th) {
  background: #0F0F11;
  border-bottom-color: #27272A;
}

.per-class__th--num { text-align: left; }

.per-class__th-inner { display: inline-flex; align-items: center; gap: 5px; }

.per-class__th:hover { color: var(--ds-text-primary); }

.per-class__sort-icon {
  opacity: 0.4;
  transition: opacity 0.2s ease, color 0.2s ease;
}

.per-class__sort-icon--active {
  opacity: 1;
  color: var(--ds-primary-500);
}

/* Row entry animation */
.per-class__row {
  opacity: 0;
  transform: translateX(-8px);
  transition: opacity 0.35s ease, transform 0.35s ease, background 0.15s ease;
}

.per-class__row--in {
  opacity: 1;
  transform: translateX(0);
}

.per-class__row:hover { background: var(--ds-neutral-50); }
:global(.dark .per-class__row:hover) { background: #1F1F23; }

.per-class__row td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--ds-border);
  color: var(--ds-text-primary);
  vertical-align: middle;
}

:global(.dark .per-class__row td) { border-bottom-color: #27272A; }

.per-class__row:last-child td { border-bottom: none; }

.per-class__cell-class { width: 190px; }

/* Category chip — editorial with dot */
.per-class__cat {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px;
  border-radius: 3px;
  background: var(--ds-surface-raised);
  border: 1px solid var(--ds-border);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  color: var(--ds-text-primary);
}

:global(.dark .per-class__cat) {
  background: #0F0F11;
  border-color: #27272A;
}

.per-class__cat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.per-class__cat--ACCOUNT      .per-class__cat-dot { background: var(--ds-cat-account); }
.per-class__cat--CANCEL       .per-class__cat-dot { background: var(--ds-cat-cancel); }
.per-class__cat--CONTACT      .per-class__cat-dot { background: var(--ds-cat-contact); }
.per-class__cat--DELIVERY     .per-class__cat-dot { background: var(--ds-cat-delivery); }
.per-class__cat--FEEDBACK     .per-class__cat-dot { background: var(--ds-cat-feedback); }
.per-class__cat--INVOICE      .per-class__cat-dot { background: var(--ds-cat-invoice); }
.per-class__cat--ORDER        .per-class__cat-dot { background: var(--ds-cat-order); }
.per-class__cat--PAYMENT      .per-class__cat-dot { background: var(--ds-cat-payment); }
.per-class__cat--REFUND       .per-class__cat-dot { background: var(--ds-cat-refund); }
.per-class__cat--SHIPPING     .per-class__cat-dot { background: var(--ds-cat-shipping); }
.per-class__cat--SUBSCRIPTION .per-class__cat-dot { background: var(--ds-cat-subscription); }

/* Inline meters */
.per-class__metric-cell { min-width: 140px; }

.per-class__meter {
  display: grid;
  grid-template-columns: 1fr 52px;
  align-items: center;
  gap: 10px;
}

.per-class__meter-track {
  height: 6px;
  background: var(--ds-neutral-100);
  border-radius: 2px;
  overflow: hidden;
}

:global(.dark .per-class__meter-track) { background: #27272A; }

.per-class__meter-track--strong { height: 8px; }

.per-class__meter-fill {
  height: 100%;
  transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.per-class__meter-fill--precision { background: var(--ds-text-secondary); }
.per-class__meter-fill--recall    { background: var(--ds-text-primary); }
.per-class__meter-fill--f1        { background: var(--ds-primary-500); }

.per-class__metric-val {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  color: var(--ds-text-secondary);
  text-align: right;
  letter-spacing: -0.02em;
}

.per-class__metric-val--bold {
  color: var(--ds-text-primary);
  font-weight: 700;
}

/* Support — different treatment: neutral outline bar */
.per-class__support {
  display: grid;
  grid-template-columns: 1fr 40px;
  align-items: center;
  gap: 10px;
  min-width: 120px;
}

.per-class__support-bar {
  height: 4px;
  background: transparent;
  border: 1px solid var(--ds-border);
  border-radius: 2px;
  overflow: hidden;
}

.per-class__support-fill {
  height: 100%;
  background: var(--ds-text-primary);
  transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.per-class__support-val {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  color: var(--ds-text-primary);
  text-align: right;
}

@media (prefers-reduced-motion: reduce) {
  .per-class__row,
  .per-class__meter-fill,
  .per-class__support-fill {
    transition: none;
  }
}
</style>
