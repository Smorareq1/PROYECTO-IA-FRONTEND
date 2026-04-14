<script setup lang="ts">
import { useTheme } from '@/core/composables/useTheme'
import { Moon, Sun } from 'lucide-vue-next'

const { isDark, toggleDark } = useTheme()
</script>

<template>
  <button
    @click="toggleDark()"
    class="theme-toggle"
    :aria-label="isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
    :title="isDark ? 'Modo claro' : 'Modo oscuro'"
  >
    <Transition name="theme-icon" mode="out-in">
      <Moon v-if="!isDark" :size="18" class="theme-toggle__icon" />
      <Sun v-else :size="18" class="theme-toggle__icon" />
    </Transition>
  </button>
</template>

<style scoped>
.theme-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--ds-radius-md);
  border: 1px solid var(--ds-border);
  background: var(--ds-surface);
  color: var(--ds-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

:global(.dark .theme-toggle) {
  background: #18181B;
  border-color: #27272A;
  color: #A1A1AA;
}

.theme-toggle:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
  border-color: var(--ds-neutral-300);
}

:global(.dark .theme-toggle:hover) {
  background: #27272A;
  border-color: #3F3F46;
  color: #FAFAFA;
}

.theme-toggle:active {
  transform: scale(0.95);
}

.theme-toggle__icon {
  transition: transform 0.2s ease;
}

/* Icon transition */
.theme-icon-enter-active,
.theme-icon-leave-active {
  transition: all 0.2s ease;
}

.theme-icon-enter-from {
  opacity: 0;
  transform: rotate(-90deg) scale(0.5);
}

.theme-icon-leave-to {
  opacity: 0;
  transform: rotate(90deg) scale(0.5);
}
</style>
