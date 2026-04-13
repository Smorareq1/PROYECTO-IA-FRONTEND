<script setup lang="ts">
import AppLogo from '@/design-system/components/AppLogo.vue'
import ThemeToggle from '@/design-system/layouts/components/ThemeToggle.vue'
import HeroSection from '../widgets/HeroSection.vue'
import FeaturesGrid from '../widgets/FeaturesGrid.vue'
import TechStackStrip from '../widgets/TechStackStrip.vue'
import { LogIn } from 'lucide-vue-next'
</script>

<template>
  <div class="landing">
    <!-- Navigation -->
    <header class="landing__nav">
      <div class="landing__nav-inner">
        <AppLogo />
        <div class="landing__nav-right">
          <ThemeToggle />
          <router-link to="/login" class="landing__login-btn">
            <LogIn :size="16" />
            <span>Iniciar sesión</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <HeroSection />

    <!-- Tech Stack -->
    <TechStackStrip />

    <!-- Features -->
    <FeaturesGrid />

    <!-- Footer -->
    <footer class="landing__footer">
      <div class="landing__footer-inner">
        <p class="landing__footer-text">
          TicketAI — Proyecto de Inteligencia Artificial · URL · 2026
        </p>
        <p class="landing__footer-sub">
          Clasificación de solicitudes con Naïve Bayes
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
}

.landing__nav {
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid var(--ds-border);
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.85);
}

:global(.dark) .landing__nav {
  background: rgba(22, 22, 22, 0.85);
}

.landing__nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 48px;
  height: 56px;
}

.landing__nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.landing__login-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: var(--ds-radius-md);
  background: var(--ds-primary-500);
  color: #fff;
  font-size: var(--ds-text-sm);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.landing__login-btn:hover {
  background: var(--ds-primary-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 98, 254, 0.3);
}

.landing__footer {
  border-top: 1px solid var(--ds-border);
  padding: 48px;
  text-align: center;
}

.landing__footer-inner {
  max-width: 1320px;
  margin: 0 auto;
}

.landing__footer-text {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  font-weight: 500;
}

.landing__footer-sub {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin-top: 4px;
}

@media (max-width: 768px) {
  .landing__nav-inner {
    padding: 0 16px;
  }

  .landing__login-btn span {
    display: none;
  }

  .landing__footer {
    padding: 32px 16px;
  }
}
</style>
