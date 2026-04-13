<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LogIn, Mail, Lock, Eye, EyeOff } from 'lucide-vue-next'
import ThemeToggle from '@/design-system/layouts/components/ThemeToggle.vue'

const router = useRouter()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor ingresa tu email y contraseña.'
    return
  }

  isLoading.value = true

  try {
    // TODO: Replace with actual API call
    // For now, simulate a login
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Simulate successful login
    localStorage.setItem('ticket_ai_access_token', 'demo-token')
    localStorage.setItem('ticket_ai_refresh_token', 'demo-refresh')
    localStorage.setItem('ticket_ai_user', JSON.stringify({
      id: '1',
      email: email.value,
      full_name: 'Usuario Demo',
      role: 'admin',
    }))

    router.push('/app')
  } catch (error) {
    errorMessage.value = 'Credenciales incorrectas. Intenta de nuevo.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-page__header">
      <div class="login-page__top-row">
        <h2 class="login-page__title">Iniciar sesión</h2>
        <ThemeToggle />
      </div>
      <p class="login-page__subtitle">Ingresa tus credenciales para acceder al sistema</p>
    </div>

    <form @submit.prevent="handleLogin" class="login-form">
      <!-- Email -->
      <div class="form-group">
        <label for="email" class="form-label">Correo electrónico</label>
        <div class="form-input-wrapper">
          <Mail :size="16" class="form-input-icon" />
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-input"
            placeholder="tu@email.com"
            autocomplete="email"
          />
        </div>
      </div>

      <!-- Password -->
      <div class="form-group">
        <label for="password" class="form-label">Contraseña</label>
        <div class="form-input-wrapper">
          <Lock :size="16" class="form-input-icon" />
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="••••••••"
            autocomplete="current-password"
          />
          <button
            type="button"
            class="form-input-toggle"
            @click="showPassword = !showPassword"
            :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
          >
            <EyeOff v-if="showPassword" :size="16" />
            <Eye v-else :size="16" />
          </button>
        </div>
      </div>

      <!-- Error -->
      <div v-if="errorMessage" class="login-error">
        {{ errorMessage }}
      </div>

      <!-- Submit -->
      <button type="submit" class="login-btn" :disabled="isLoading">
        <LogIn v-if="!isLoading" :size="16" />
        <svg v-else class="login-spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        </svg>
        <span>{{ isLoading ? 'Ingresando...' : 'Iniciar sesión' }}</span>
      </button>
    </form>

    <div class="login-page__footer">
      <p class="login-page__demo">
        Demo: usa cualquier email y contraseña
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  width: 100%;
  max-width: 400px;
}

.login-page__header {
  margin-bottom: 32px;
}

.login-page__top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.login-page__title {
  font-size: var(--ds-text-2xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.02em;
}

.login-page__subtitle {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-muted);
  margin-top: 4px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: var(--ds-text-sm);
  font-weight: 500;
  color: var(--ds-text-primary);
}

.form-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input-icon {
  position: absolute;
  left: 12px;
  color: var(--ds-text-muted);
  pointer-events: none;
  z-index: 1;
}

.form-input {
  width: 100%;
  padding: 10px 12px 10px 38px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-base);
  font-family: var(--ds-font-sans);
  transition: all 0.2s ease;
  outline: none;
}

.form-input::placeholder {
  color: var(--ds-text-muted);
}

.form-input:focus {
  border-color: var(--ds-primary-500);
  box-shadow: 0 0 0 3px rgba(15, 98, 254, 0.1);
}

.form-input-toggle {
  position: absolute;
  right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--ds-text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: var(--ds-radius-sm);
  transition: color 0.15s ease;
}

.form-input-toggle:hover {
  color: var(--ds-text-primary);
}

.login-error {
  padding: 10px 14px;
  background: var(--ds-cat-queja-bg);
  color: var(--ds-danger);
  border: 1px solid rgba(218, 30, 40, 0.2);
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px 24px;
  background: var(--ds-primary-500);
  color: #fff;
  border: none;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-base);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-btn:hover:not(:disabled) {
  background: var(--ds-primary-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 98, 254, 0.3);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-page__footer {
  margin-top: 32px;
  text-align: center;
}

.login-page__demo {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  padding: 8px 16px;
  background: var(--ds-neutral-50);
  border-radius: var(--ds-radius-md);
  border: 1px dashed var(--ds-border);
}
</style>
