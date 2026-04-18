<script setup lang="ts">
import { RouterLink } from 'vue-router'
import AppLogo from '@/design-system/atoms/AppLogo.vue'
import ThemeToggle from '@/design-system/atoms/ThemeToggle.vue'

const navItems = [
  { label: 'Cola', to: '/app/cola' },
  { label: 'Playground', to: '/app/playground' },
  { label: 'Dashboard', to: '/app/dashboard' },
]
</script>

<template>
  <header class="topbar">
    <div class="topbar__inner">
      <div class="topbar__left">
        <AppLogo />
      </div>

      <nav class="topbar__nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="topbar__nav-link"
          active-class="topbar__nav-link--active"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="topbar__right">
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid var(--ds-border);
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.85);
}

:global(.dark .topbar) {
  background: rgba(9, 9, 11, 0.9);
  border-bottom-color: #27272A;
}

.topbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 32px;
  height: 56px;
  gap: 16px;
}

.topbar__nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  justify-content: center;
}

.topbar__nav-link {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 12px;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 500;
  color: var(--ds-text-secondary);
  text-decoration: none;
  transition: all 0.15s;
}

.topbar__nav-link:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
}

:global(.dark .topbar__nav-link:hover) { background: #27272A; }

.topbar__nav-link--active {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
  font-weight: 600;
}

:global(.dark .topbar__nav-link--active) { background: #27272A; }

.topbar__right {
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .topbar__inner { padding: 0 16px; }
  .topbar__nav { display: none; }
}
</style>
