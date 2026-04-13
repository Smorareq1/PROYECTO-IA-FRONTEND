<script setup lang="ts">
import { ShieldAlert } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="unauthorized">
    <div class="unauthorized__icon">
      <ShieldAlert :size="48" />
    </div>
    <h1 class="unauthorized__title">Acceso Denegado</h1>
    <p class="unauthorized__message">
      No tienes permisos para acceder a esta sección.
    </p>
    <button @click="router.push('/')" class="unauthorized__btn">
      Volver al inicio
    </button>
  </div>
</template>

<style scoped>
.unauthorized {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 48px 24px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.unauthorized__icon {
  color: var(--ds-danger);
  margin-bottom: 16px;
  opacity: 0.7;
}

.unauthorized__title {
  font-size: var(--ds-text-2xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  margin-bottom: 8px;
}

.unauthorized__message {
  font-size: var(--ds-text-base);
  color: var(--ds-text-muted);
  margin-bottom: 32px;
}

.unauthorized__btn {
  padding: 10px 20px;
  background: var(--ds-primary-500);
  color: #fff;
  border: none;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--ds-font-sans);
}

.unauthorized__btn:hover {
  background: var(--ds-primary-600);
  transform: translateY(-1px);
}
</style>
