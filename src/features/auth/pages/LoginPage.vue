<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { LogIn, Mail, Lock, Eye, EyeOff } from 'lucide-vue-next'
import { animList, stagger } from '@/core/composables/useMotionAnimate'
import ThemeToggle from '@/design-system/layouts/components/ThemeToggle.vue'

const router = useRouter()

const email        = ref('')
const password     = ref('')
const showPassword = ref(false)
const isLoading    = ref(false)
const errorMessage = ref('')

const pageRef = ref<HTMLElement>()

onMounted(() => {
  if (!pageRef.value) return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) return

  const easeOut = [0.22, 1, 0.36, 1] as const
  const els = pageRef.value.querySelectorAll<HTMLElement>('.login-anim')
  // Set initial state via JS (progressive enhancement)
  els.forEach(el => { el.style.opacity = '0' })

  requestAnimationFrame(() => {
    animList(els, { opacity: [0, 1], y: [18, 0] }, { delay: stagger(0.09, { startDelay: 0.05 }), duration: 0.45, easing: easeOut })
  })
})

async function handleLogin() {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor ingresa tu email y contraseña.'
    return
  }

  isLoading.value = true

  try {
    await new Promise(resolve => setTimeout(resolve, 1000))

    localStorage.setItem('ticket_ai_access_token', 'demo-token')
    localStorage.setItem('ticket_ai_refresh_token', 'demo-refresh')
    localStorage.setItem('ticket_ai_user', JSON.stringify({
      id: '1',
      email: email.value,
      full_name: 'Usuario Demo',
      role: 'admin',
    }))

    router.push('/app')
  } catch {
    errorMessage.value = 'Credenciales incorrectas. Intenta de nuevo.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page" ref="pageRef">

    <!-- Header -->
    <div class="login-anim login-page__header">
      <div class="login-page__top-row">
        <div>
          <h2 class="login-page__title">Iniciar sesión</h2>
          <p class="login-page__subtitle">Ingresa tus credenciales para acceder</p>
        </div>
        <ThemeToggle />
      </div>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleLogin" class="login-form" novalidate>

      <!-- Email -->
      <div class="login-anim form-group">
        <label for="email" class="form-label">Correo electrónico</label>
        <div class="form-input-wrapper">
          <Mail :size="15" class="form-input-icon" aria-hidden="true" />
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-input"
            placeholder="tu@email.com"
            autocomplete="email"
            :aria-invalid="!!errorMessage"
          />
        </div>
      </div>

      <!-- Password -->
      <div class="login-anim form-group">
        <label for="password" class="form-label">Contraseña</label>
        <div class="form-input-wrapper">
          <Lock :size="15" class="form-input-icon" aria-hidden="true" />
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="••••••••"
            autocomplete="current-password"
            :aria-invalid="!!errorMessage"
          />
          <button
            type="button"
            class="form-input-toggle"
            @click="showPassword = !showPassword"
            :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
          >
            <EyeOff v-if="showPassword" :size="15" />
            <Eye v-else :size="15" />
          </button>
        </div>
      </div>

      <!-- Error -->
      <Transition name="slide-error">
        <div v-if="errorMessage" class="login-anim login-error" role="alert" aria-live="polite">
          {{ errorMessage }}
        </div>
      </Transition>

      <!-- Submit -->
      <div class="login-anim">
        <button type="submit" class="login-btn" :disabled="isLoading">
          <svg
            v-if="isLoading"
            class="login-spinner"
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            aria-hidden="true"
          >
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
          <LogIn v-else :size="15" aria-hidden="true" />
          <span>{{ isLoading ? 'Ingresando…' : 'Iniciar sesión' }}</span>
        </button>
      </div>
    </form>

    <!-- Footer -->
    <div class="login-anim login-page__footer">
      <p class="login-page__demo">
        Demo: usa cualquier email y contraseña
      </p>
    </div>
  </div>
</template>

<style scoped>
/* ── Page shell ──────────────────────────────────────────── */
.login-page {
  width: 100%;
  max-width: 400px;
}

/* ── Header ──────────────────────────────────────────────── */
.login-page__header {
  margin-bottom: 32px;
}

.login-page__top-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.login-page__title {
  font-size: var(--ds-text-2xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.025em;
  line-height: 1.2;
  margin-bottom: 4px;
}

.login-page__subtitle {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-muted);
}

/* ── Form ────────────────────────────────────────────────── */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
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
  transition: color 0.15s ease;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 12px 0 38px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-base);
  font-family: var(--ds-font-sans);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  outline: none;
}

.form-input::placeholder {
  color: var(--ds-text-muted);
}

.form-input:focus {
  border-color: var(--ds-primary-500);
  box-shadow: 0 0 0 3px rgba(15, 98, 254, 0.12);
}

.form-input:focus + .form-input-icon,
.form-input-wrapper:focus-within .form-input-icon {
  color: var(--ds-primary-500);
}

.form-input[aria-invalid="true"] {
  border-color: var(--ds-danger);
}

.form-input[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px rgba(218, 30, 40, 0.12);
}

.form-input-toggle {
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  color: var(--ds-text-muted);
  cursor: pointer;
  border-radius: var(--ds-radius-sm);
  transition: color 0.15s ease, background 0.15s ease;
}

.form-input-toggle:hover {
  color: var(--ds-text-primary);
  background: var(--ds-neutral-100);
}

/* ── Error ───────────────────────────────────────────────── */
.login-error {
  padding: 10px 14px;
  background: var(--ds-cat-queja-bg);
  color: var(--ds-danger);
  border: 1px solid rgba(218, 30, 40, 0.2);
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  line-height: 1.4;
}

.slide-error-enter-active {
  animation: slideErrorIn 0.22s ease-out;
}

.slide-error-leave-active {
  animation: slideErrorIn 0.18s ease-in reverse;
}

@keyframes slideErrorIn {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Submit button ───────────────────────────────────────── */
.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 44px;
  background: var(--ds-primary-500);
  color: #fff;
  border: none;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-base);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

.login-btn:hover:not(:disabled) {
  background: var(--ds-primary-600);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(15, 98, 254, 0.3);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: none;
}

.login-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.login-spinner {
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ── Footer ──────────────────────────────────────────────── */
.login-page__footer {
  margin-top: 28px;
  text-align: center;
}

.login-page__demo {
  display: inline-block;
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  padding: 7px 16px;
  background: var(--ds-neutral-50);
  border-radius: var(--ds-radius-md);
  border: 1px dashed var(--ds-border);
  line-height: 1.4;
}

@media (prefers-reduced-motion: reduce) {
  .login-spinner {
    animation: none;
  }
}
</style>
