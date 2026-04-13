<script setup lang="ts">
</script>

<template>
  <div class="auth-layout">
    <div class="auth-layout__left">
      <div class="auth-layout__branding">
        <div class="auth-layout__logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 4.5a2.5 2.5 0 0 0-4.96-.46 2.5 2.5 0 0 0-1.98 3 2.5 2.5 0 0 0-1.32 4.24 3 3 0 0 0 .34 5.58 2.5 2.5 0 0 0 2.96 3.08A2.5 2.5 0 0 0 12 19.5a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 12 4.5"/>
            <path d="m15.7 10.4-.9.4"/>
            <path d="m9.2 13.2-.9.4"/>
            <path d="m13.6 15.7-.4-.9"/>
            <path d="m10.8 9.2-.4-.9"/>
            <path d="m15.7 13.5-.9-.4"/>
            <path d="m9.2 10.9-.9-.4"/>
            <path d="m10.5 15.7.4-.9"/>
            <path d="m13.1 9.2.4-.9"/>
          </svg>
        </div>
        <h1 class="auth-layout__title">TicketAI</h1>
        <p class="auth-layout__subtitle">
          Clasificación inteligente de tickets<br />
          con Naïve Bayes
        </p>
        <div class="auth-layout__features">
          <div class="auth-layout__feature">
            <span class="auth-layout__feature-dot"></span>
            Clasificación automática por categoría
          </div>
          <div class="auth-layout__feature">
            <span class="auth-layout__feature-dot"></span>
            Análisis de confianza en tiempo real
          </div>
          <div class="auth-layout__feature">
            <span class="auth-layout__feature-dot"></span>
            Dashboard con métricas del modelo
          </div>
        </div>
      </div>
    </div>
    <div class="auth-layout__right">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  display: flex;
  min-height: 100vh;
}

.auth-layout__left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a1628 0%, #0F62FE 50%, #4589FF 100%);
  color: #fff;
  padding: 48px;
  position: relative;
  overflow: hidden;
}

.auth-layout__left::before {
  content: '';
  position: absolute;
  top: -30%;
  right: -20%;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
}

.auth-layout__left::after {
  content: '';
  position: absolute;
  bottom: -20%;
  left: -10%;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
}

.auth-layout__branding {
  position: relative;
  z-index: 1;
  max-width: 400px;
}

.auth-layout__logo-icon {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--ds-radius-xl);
  backdrop-filter: blur(8px);
  margin-bottom: 32px;
}

.auth-layout__title {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  margin-bottom: 12px;
  line-height: 1;
}

.auth-layout__subtitle {
  font-size: 1.125rem;
  opacity: 0.75;
  line-height: 1.6;
  margin-bottom: 48px;
}

.auth-layout__features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.auth-layout__feature {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.875rem;
  opacity: 0.8;
}

.auth-layout__feature-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4589FF;
  flex-shrink: 0;
  box-shadow: 0 0 8px rgba(69, 137, 255, 0.5);
}

.auth-layout__right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: var(--ds-surface);
}

@media (max-width: 768px) {
  .auth-layout {
    flex-direction: column;
  }

  .auth-layout__left {
    padding: 32px 24px;
    min-height: auto;
  }

  .auth-layout__features {
    display: none;
  }

  .auth-layout__right {
    padding: 24px;
  }
}
</style>
