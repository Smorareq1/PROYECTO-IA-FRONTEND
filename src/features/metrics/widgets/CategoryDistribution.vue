<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import type { ClassMetrics } from '../models/metrics'
import { CATEGORY_LABELS } from '@/core/config/constants'

const props = defineProps<{ metrics: ClassMetrics[] }>()

const animatedIn = ref(false)
onMounted(() => { requestAnimationFrame(() => { animatedIn.value = true }) })

const COLORS: Record<string, string> = {
  soporte_tecnico:  'var(--ds-cat-soporte)',
  facturacion:      'var(--ds-cat-facturacion)',
  consulta_general: 'var(--ds-cat-consulta)',
  queja:            'var(--ds-cat-queja)',
  cancelacion:      'var(--ds-cat-cancelacion)',
}

const total = computed(() => props.metrics.reduce((sum, m) => sum + m.support, 0))

const sorted = computed(() =>
  [...props.metrics].sort((a, b) => b.support - a.support),
)

const maxSupport = computed(() =>
  Math.max(...props.metrics.map(m => m.support), 1),
)

function pctOfTotal(support: number) {
  return total.value === 0 ? 0 : (support / total.value) * 100
}
</script>

<template>
  <div class="cat-dist">
    <div class="cat-dist__header">
      <span class="cat-dist__label">Total de muestras</span>
      <span class="cat-dist__total">{{ total.toLocaleString() }}</span>
    </div>

    <ul class="cat-dist__list">
      <li
        v-for="(m, i) in sorted"
        :key="m.class"
        class="cat-dist__row"
        :class="{ 'cat-dist__row--in': animatedIn }"
        :style="{ transitionDelay: `${i * 60}ms` }"
      >
        <div class="cat-dist__row-top">
          <div class="cat-dist__name">
            <span class="cat-dist__dot" :style="{ background: COLORS[m.class] ?? '#999' }"></span>
            <span>{{ CATEGORY_LABELS[m.class] }}</span>
          </div>
          <div class="cat-dist__values">
            <span class="cat-dist__count">{{ m.support.toLocaleString() }}</span>
            <span class="cat-dist__pct">{{ pctOfTotal(m.support).toFixed(1) }}%</span>
          </div>
        </div>
        <div class="cat-dist__track">
          <div
            class="cat-dist__fill"
            :style="{
              width: animatedIn ? `${(m.support / maxSupport) * 100}%` : '0%',
              background: COLORS[m.class] ?? '#999',
              transitionDelay: `${i * 60 + 100}ms`,
            }"
          ></div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.cat-dist {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  padding: 18px 20px 20px;
}

:global(.dark .cat-dist) { background: #18181B; border-color: #27272A; }

.cat-dist__header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding-bottom: 14px;
  margin-bottom: 14px;
  border-bottom: 1px dashed var(--ds-border);
}

:global(.dark .cat-dist__header) { border-bottom-color: #27272A; }

.cat-dist__label {
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ds-text-muted);
}

.cat-dist__total {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xl);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--ds-text-primary);
}

.cat-dist__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.cat-dist__row {
  opacity: 0;
  transform: translateX(-6px);
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.cat-dist__row--in { opacity: 1; transform: translateX(0); }

.cat-dist__row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.cat-dist__name {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.cat-dist__dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

.cat-dist__values {
  display: inline-flex;
  align-items: baseline;
  gap: 8px;
}

.cat-dist__count {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-sm);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.02em;
}

.cat-dist__pct {
  font-family: var(--ds-font-mono);
  font-size: 0.6875rem;
  color: var(--ds-text-muted);
  font-weight: 600;
}

.cat-dist__track {
  height: 8px;
  background: var(--ds-neutral-100);
  border-radius: 2px;
  overflow: hidden;
}

:global(.dark .cat-dist__track) { background: #27272A; }

.cat-dist__fill {
  height: 100%;
  width: 0%;
  transition: width 0.85s cubic-bezier(0.22, 1, 0.36, 1);
}

@media (prefers-reduced-motion: reduce) {
  .cat-dist__row,
  .cat-dist__fill { transition: none; }
}
</style>
