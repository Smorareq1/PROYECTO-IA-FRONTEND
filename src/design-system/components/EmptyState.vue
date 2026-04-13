<script setup lang="ts">
import { Inbox } from 'lucide-vue-next'

interface Props {
  title?: string
  message?: string
}

withDefaults(defineProps<Props>(), {
  title: 'Sin resultados',
  message: 'No se encontraron datos para mostrar.',
})
</script>

<template>
  <div class="empty-state">
    <div class="empty-state__icon">
      <slot name="icon">
        <Inbox :size="48" />
      </slot>
    </div>
    <h3 class="empty-state__title">{{ title }}</h3>
    <p class="empty-state__message">{{ message }}</p>
    <div v-if="$slots.action" class="empty-state__action">
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 64px 24px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.empty-state__icon {
  color: var(--ds-neutral-300);
  margin-bottom: 16px;
}

.empty-state__title {
  font-size: var(--ds-text-lg);
  font-weight: 600;
  color: var(--ds-text-primary);
  margin-bottom: 4px;
}

.empty-state__message {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-muted);
  max-width: 360px;
}

.empty-state__action {
  margin-top: 24px;
}
</style>
