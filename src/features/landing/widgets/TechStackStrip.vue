<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { animList, stagger } from '@/core/composables/useMotionAnimate'
import {
  Layers2,
  FileCode2,
  Zap,
  BrainCircuit,
  Paintbrush2,
  BarChart2,
  Package2,
  ShieldCheck,
} from 'lucide-vue-next'

const techItems = [
  { name: 'Vue 3',        icon: Layers2,      color: '#42b883' },
  { name: 'TypeScript',   icon: FileCode2,    color: '#3178c6' },
  { name: 'FastAPI',      icon: Zap,          color: '#059669' },
  { name: 'Naïve Bayes',  icon: BrainCircuit, color: '#8A3FFC' },
  { name: 'Tailwind CSS', icon: Paintbrush2,  color: '#0ea5e9' },
  { name: 'ECharts',      icon: BarChart2,    color: '#0F62FE' },
  { name: 'Pinia',        icon: Package2,     color: '#f59e0b' },
  { name: 'Zod',          icon: ShieldCheck,  color: '#10b981' },
]

const stripRef = ref<HTMLElement>()

onMounted(() => {
  if (!stripRef.value) return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) return

  const items = stripRef.value.querySelectorAll<HTMLElement>('.tech-strip__item')
  items.forEach(el => { el.style.opacity = '0' })
  requestAnimationFrame(() => {
    animList(
      items,
      { opacity: [0, 1], y: [12, 0] },
      { delay: stagger(0.07), duration: 0.4, easing: [0.22, 1, 0.36, 1] },
    )
  })
})
</script>

<template>
  <section class="tech-strip">
    <div class="tech-strip__inner" ref="stripRef">
      <span class="tech-strip__label">Construido con</span>
      <div class="tech-strip__items">
        <div
          v-for="item in techItems"
          :key="item.name"
          class="tech-strip__item"
          :style="{ '--item-color': item.color }"
        >
          <component
            :is="item.icon"
            :size="14"
            class="tech-strip__icon"
          />
          <span class="tech-strip__name">{{ item.name }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.tech-strip {
  border-top: 1px solid var(--ds-border);
  border-bottom: 1px solid var(--ds-border);
  background: var(--ds-surface-raised);
}

.tech-strip__inner {
  max-width: 1320px;
  margin: 0 auto;
  padding: 20px 48px;
  display: flex;
  align-items: center;
  gap: 28px;
}

.tech-strip__label {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.tech-strip__items {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.tech-strip__item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: var(--ds-radius-sm);
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  font-size: var(--ds-text-xs);
  font-weight: 500;
  color: var(--ds-text-secondary);
  cursor: default;
  transition: border-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

:global(.dark .tech-strip) {
  background: #0C0C0E;
  border-color: #27272A;
}

:global(.dark .tech-strip__item) {
  background: #18181B;
  border-color: #27272A;
}

.tech-strip__icon {
  color: var(--item-color);
  flex-shrink: 0;
}

.tech-strip__item:hover {
  border-color: var(--item-color);
  color: var(--item-color);
  transform: translateY(-1px);
}

.tech-strip__name {
  letter-spacing: 0.01em;
}

@media (max-width: 768px) {
  .tech-strip__inner {
    flex-direction: column;
    padding: 20px 16px;
    gap: 12px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .tech-strip__item {
    transition: none;
  }
}
</style>
