<script setup lang="ts">
import { useToast, type Toast } from '@/core/composables/useToast'
import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-vue-next'
import { computed } from 'vue'

const { toasts, removeToast } = useToast()

function getIcon(type: Toast['type']) {
  switch (type) {
    case 'success': return CheckCircle
    case 'error': return XCircle
    case 'warning': return AlertTriangle
    case 'info': return Info
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="toast-container" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast"
          :class="[`toast--${toast.type}`]"
          role="alert"
        >
          <div class="toast__icon">
            <component :is="getIcon(toast.type)" :size="18" />
          </div>
          <div class="toast__content">
            <p class="toast__title">{{ toast.title }}</p>
            <p v-if="toast.message" class="toast__message">{{ toast.message }}</p>
          </div>
          <button class="toast__close" @click="removeToast(toast.id)" aria-label="Cerrar">
            <X :size="14" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 420px;
  width: 100%;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  box-shadow: var(--ds-shadow-lg);
  pointer-events: auto;
  position: relative;
  overflow: hidden;
}

:global(.dark .toast) {
  background: #1C1C1F;
  border-color: #27272A;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
}

.toast::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
}

.toast--success::before { background: var(--ds-success); }
.toast--error::before   { background: var(--ds-danger); }
.toast--warning::before { background: var(--ds-warning); }
.toast--info::before    { background: var(--ds-info); }

.toast__icon {
  flex-shrink: 0;
  margin-top: 1px;
}

.toast--success .toast__icon { color: var(--ds-success); }
.toast--error .toast__icon   { color: var(--ds-danger); }
.toast--warning .toast__icon { color: var(--ds-warning); }
.toast--info .toast__icon    { color: var(--ds-info); }

.toast__content {
  flex: 1;
  min-width: 0;
}

.toast__title {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.toast__message {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-secondary);
  margin-top: 2px;
}

.toast__close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  color: var(--ds-text-muted);
  cursor: pointer;
  border-radius: var(--ds-radius-sm);
  transition: all 0.15s ease;
}

.toast__close:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-text-primary);
}

:global(.dark .toast__close:hover) {
  background: #27272A;
}

/* Transitions */
.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.2s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
