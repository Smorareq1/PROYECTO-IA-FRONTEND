<script setup lang="ts">
const techItems = [
  { name: 'Vue 3', icon: '🟢' },
  { name: 'TypeScript', icon: '🔷' },
  { name: 'FastAPI', icon: '⚡' },
  { name: 'Naïve Bayes', icon: '🧠' },
  { name: 'Tailwind CSS', icon: '🎨' },
  { name: 'ECharts', icon: '📊' },
  { name: 'Pinia', icon: '🍍' },
  { name: 'Zod', icon: '✅' },
]
</script>

<template>
  <section class="tech-strip">
    <div class="tech-strip__inner">
      <span class="tech-strip__label">Construido con</span>
      <div class="tech-strip__items">
        <div
          v-for="item in techItems"
          :key="item.name"
          class="tech-strip__item"
        >
          <span class="tech-strip__emoji">{{ item.icon }}</span>
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
  padding: 24px 48px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.tech-strip__label {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  white-space: nowrap;
}

.tech-strip__items {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tech-strip__item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--ds-radius-full);
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  font-size: var(--ds-text-xs);
  font-weight: 500;
  color: var(--ds-text-secondary);
  transition: all 0.2s ease;
}

.tech-strip__item:hover {
  border-color: var(--ds-primary-300);
  color: var(--ds-primary-500);
  transform: translateY(-2px);
  box-shadow: var(--ds-shadow-sm);
}

.tech-strip__emoji {
  font-size: 14px;
}

.tech-strip__name {
  letter-spacing: 0.01em;
}

@media (max-width: 768px) {
  .tech-strip__inner {
    flex-direction: column;
    padding: 24px;
    gap: 16px;
  }
}
</style>
