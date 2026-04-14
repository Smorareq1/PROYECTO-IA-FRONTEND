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
    <div class="stat-card__header">
      <span class="stat-card__title">{{ title }}</span>
      <div v-if="icon" class="stat-card__icon">
        <component :is="icon" :size="20" />
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
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 20px 24px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

:global(.dark .stat-card) {
  background: #18181B;
  border-color: #27272A;
}

:global(.dark .stat-card:hover) {
  border-color: #3F3F46;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--ds-neutral-200);
  transition: background 0.2s ease;
}

.stat-card:hover {
  box-shadow: var(--ds-shadow-md);
  border-color: var(--ds-neutral-300);
  transform: translateY(-2px);
}

.stat-card--primary::before { background: var(--ds-primary-500); }
.stat-card--success::before { background: var(--ds-success); }
.stat-card--warning::before { background: var(--ds-warning); }
.stat-card--danger::before  { background: var(--ds-danger); }

.stat-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.stat-card__title {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-card__icon {
  color: var(--ds-text-muted);
  opacity: 0.5;
}

.stat-card__value {
  font-size: var(--ds-text-3xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.stat-card__footer {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.stat-card__subtitle {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.stat-card__trend {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  padding: 2px 6px;
  border-radius: var(--ds-radius-sm);
}

.stat-card__trend--up {
  color: var(--ds-success);
  background: rgba(25, 128, 56, 0.1);
}

.stat-card__trend--down {
  color: var(--ds-danger);
  background: rgba(218, 30, 40, 0.1);
}
</style>
