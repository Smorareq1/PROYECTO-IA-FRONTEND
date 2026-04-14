<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'

interface Props {
  title: string
  value: string | number
  subtitle?: string
  trend?: number
  icon?: Component
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
})

const trendClass = computed(() => {
  if (!props.trend) return ''
  return props.trend > 0 ? 'stat-card__trend--up' : 'stat-card__trend--down'
})

const trendText = computed(() => {
  if (!props.trend) return ''
  const sign = props.trend > 0 ? '+' : ''
  return `${sign}${props.trend.toFixed(1)}%`
})
</script>

<template>
  <div class="stat-card" :class="[`stat-card--${variant}`]">
    <div class="stat-card__accent" aria-hidden="true"></div>

    <div class="stat-card__header">
      <span class="stat-card__title">{{ title }}</span>
      <div v-if="icon" class="stat-card__icon">
        <component :is="icon" :size="18" />
      </div>
    </div>

    <div class="stat-card__value">{{ value }}</div>

    <div class="stat-card__footer">
      <span v-if="subtitle" class="stat-card__subtitle">{{ subtitle }}</span>
      <span v-if="trend" class="stat-card__trend" :class="trendClass">
        {{ trendText }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  position: relative;
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  padding: 22px 22px 20px;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}

:global(.dark .stat-card) {
  background: #18181B;
  border-color: #27272A;
}

/* Left accent rule — editorial Swiss */
.stat-card__accent {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
  background: var(--ds-neutral-200);
  transition: background 0.2s ease;
}

:global(.dark .stat-card__accent) { background: #27272A; }

.stat-card--primary .stat-card__accent { background: var(--ds-primary-500); }
.stat-card--success .stat-card__accent { background: var(--ds-success); }
.stat-card--warning .stat-card__accent { background: var(--ds-warning); }
.stat-card--danger  .stat-card__accent { background: var(--ds-danger); }

.stat-card:hover {
  transform: translateY(-2px);
  border-color: var(--ds-text-primary);
  box-shadow: 0 2px 0 var(--ds-text-primary);
}

:global(.dark .stat-card:hover) {
  border-color: var(--ds-neutral-200);
  box-shadow: 0 2px 0 var(--ds-neutral-200);
}

.stat-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  gap: 8px;
}

.stat-card__title {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.stat-card__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: 1px solid var(--ds-border);
  border-radius: 3px;
  color: var(--ds-text-muted);
  background: var(--ds-surface-raised);
  transition: color 0.2s ease, border-color 0.2s ease;
}

:global(.dark .stat-card__icon) {
  background: #0F0F11;
  border-color: #27272A;
}

.stat-card--primary .stat-card__icon { color: var(--ds-primary-500); }
.stat-card--success .stat-card__icon { color: var(--ds-success); }
.stat-card--warning .stat-card__icon { color: var(--ds-warning); }
.stat-card--danger  .stat-card__icon { color: var(--ds-danger); }

.stat-card__value {
  font-family: var(--ds-font-mono);
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.03em;
  line-height: 1.05;
}

.stat-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed var(--ds-border);
}

:global(.dark .stat-card__footer) { border-top-color: #27272A; }

.stat-card__subtitle {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  line-height: 1.3;
}

.stat-card__trend {
  font-size: var(--ds-text-xs);
  font-weight: 700;
  font-family: var(--ds-font-mono);
  padding: 2px 7px;
  border-radius: 3px;
  flex-shrink: 0;
}

.stat-card__trend--up {
  color: var(--ds-success);
  border: 1px solid var(--ds-success);
}

.stat-card__trend--down {
  color: var(--ds-danger);
  border: 1px solid var(--ds-danger);
}
</style>
