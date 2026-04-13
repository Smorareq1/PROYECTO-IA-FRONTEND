<script setup lang="ts">
import { BrainCircuit } from 'lucide-vue-next'

interface Props {
  variant?: 'default' | 'light'
  showText?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'default',
  showText: true,
})
</script>

<template>
  <router-link to="/" class="app-logo" :class="[`app-logo--${variant}`]">
    <div class="app-logo__icon">
      <BrainCircuit :size="24" />
    </div>
    <div v-if="showText" class="app-logo__text">
      <span class="app-logo__name">TicketAI</span>
      <span class="app-logo__tagline">Mesa de Ayuda</span>
    </div>
  </router-link>
</template>

<style scoped>
.app-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s ease;
}

.app-logo:hover {
  opacity: 0.85;
}

.app-logo__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--ds-radius-lg);
  background: linear-gradient(135deg, var(--ds-primary-500), var(--ds-primary-700));
  color: #fff;
  flex-shrink: 0;
}

.app-logo__text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.app-logo__name {
  font-size: var(--ds-text-lg);
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--ds-text-primary);
}

.app-logo__tagline {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  font-weight: 400;
}

/* Light variant (for dark backgrounds) */
.app-logo--light .app-logo__name {
  color: #fff;
}

.app-logo--light .app-logo__tagline {
  color: rgba(255, 255, 255, 0.6);
}

.app-logo--light .app-logo__icon {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
}
</style>
