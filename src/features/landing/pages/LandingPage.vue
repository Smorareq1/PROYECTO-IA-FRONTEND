<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { animEl } from '@/core/composables/useMotionAnimate'
import AppLogo from '@/design-system/atoms/AppLogo.vue'
import ThemeToggle from '@/design-system/atoms/ThemeToggle.vue'
import HeroSection from '../widgets/HeroSection.vue'
import FeaturesGrid from '../widgets/FeaturesGrid.vue'
import TechStackStrip from '../widgets/TechStackStrip.vue'
import { LogIn } from 'lucide-vue-next'

const navRef = ref<HTMLElement>()

onMounted(() => {
  if (!navRef.value) return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) return

  // Set initial invisible state via JS so it's always visible without JS
  navRef.value.style.opacity = '0'
  navRef.value.style.transform = 'translateY(-8px)'

  requestAnimationFrame(() => {
    animEl(
      navRef.value,
      { opacity: [0, 1], y: [-8, 0] },
      { duration: 0.4, easing: [0.22, 1, 0.36, 1] },
    )
  })
})
</script>

<template>
  <div class="landing">
    <!-- Navigation -->
    <header class="landing__nav" ref="navRef">
      <div class="landing__nav-inner">
        <AppLogo />
        <div class="landing__nav-right">
          <ThemeToggle />
          <router-link to="/login" class="landing__login-btn">
            <LogIn :size="15" aria-hidden="true" />
            <span>Iniciar sesión</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main>
      <HeroSection />
      <TechStackStrip />
      <FeaturesGrid />
    </main>

    <!-- Footer -->
    <footer class="landing__footer">
      <div class="landing__footer-inner">
        <div class="landing__footer-brand">
          <AppLogo :show-text="false" />
          <p class="landing__footer-text">
            TicketAI — Proyecto de Inteligencia Artificial · URL · 2026
          </p>
        </div>
        <p class="landing__footer-sub">
          Clasificación de solicitudes con Naïve Bayes
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background-color: var(--ds-surface);
}

/* ── Nav ─────────────────────────────────────────────────── */
.landing__nav {
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid var(--ds-border);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  background: rgba(255, 255, 255, 0.82);
}

:global(.dark .landing__nav) {
  background: rgba(9, 9, 11, 0.9);
  border-bottom-color: #27272A;
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
  gap: 10px;
}

.landing__login-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 16px;
  border-radius: var(--ds-radius-md);
  background: var(--ds-primary-500);
  color: #fff;
  font-size: var(--ds-text-sm);
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

.landing__login-btn:hover {
  background: var(--ds-primary-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(15, 98, 254, 0.3);
}

.landing__login-btn:active {
  transform: translateY(0);
  box-shadow: none;
}

/* ── Footer ──────────────────────────────────────────────── */
.landing__footer {
  margin-top: auto;
  border-top: 1px solid var(--ds-border);
  padding: 32px 48px;
}

.landing__footer-inner {
  max-width: 1320px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.landing__footer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.landing__footer-text {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  font-weight: 500;
}

.landing__footer-sub {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 768px) {
  .landing__nav-inner {
    padding: 0 16px;
  }

  .landing__login-btn span {
    display: none;
  }

  .landing__footer {
    padding: 24px 16px;
  }

  .landing__footer-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

</style>
