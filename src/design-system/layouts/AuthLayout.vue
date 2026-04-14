<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { animList, stagger } from '@/core/composables/useMotionAnimate'
import { BrainCircuit, CheckCircle2, BarChart2, ShieldCheck } from 'lucide-vue-next'

const leftRef     = ref<HTMLElement>()
const brandingRef = ref<HTMLElement>()

const features = [
  { icon: BrainCircuit, text: 'Clasificación automática por categoría' },
  { icon: BarChart2,    text: 'Análisis de confianza en tiempo real'  },
  { icon: ShieldCheck,  text: 'Dashboard con métricas del modelo'      },
]

/* Mini demo data for the animated card */
const demoTickets = [
  { text: 'Cargo duplicado en mi factura',   cat: 'Facturación', pct: 94, color: '#8A3FFC', bg: 'rgba(138,63,252,0.1)' },
  { text: 'No puedo acceder a mi cuenta',    cat: 'Soporte',     pct: 91, color: '#0F62FE', bg: 'rgba(15,98,254,0.1)'  },
  { text: 'Quiero cancelar mi suscripción',  cat: 'Cancelación', pct: 88, color: '#EB6200', bg: 'rgba(235,98,0,0.1)'   },
]

onMounted(() => {
  if (!leftRef.value) return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) return

  const easeOut = [0.22, 1, 0.36, 1] as const

  // Set initial state via JS
  if (brandingRef.value) {
    brandingRef.value.querySelectorAll<HTMLElement>('.auth-anim')
      .forEach(el => { el.style.opacity = '0' })
  }
  leftRef.value.querySelectorAll<HTMLElement>('.auth-demo__row')
    .forEach(el => { el.style.opacity = '0' })

  requestAnimationFrame(() => {
    if (brandingRef.value) {
      const children = brandingRef.value.querySelectorAll('.auth-anim')
      animList(children, { opacity: [0, 1], y: [20, 0] }, { delay: stagger(0.12, { startDelay: 0.2 }), duration: 0.55, easing: easeOut })
    }
    const rows = leftRef.value!.querySelectorAll('.auth-demo__row')
    animList(rows, { opacity: [0, 1], x: [-16, 0] }, { delay: stagger(0.12, { startDelay: 0.7 }), duration: 0.45, easing: easeOut })
  })
})
</script>

<template>
  <div class="auth-layout">
    <!-- ─── Left panel ─────────────────────────── -->
    <div class="auth-layout__left" ref="leftRef">
      <!-- Decorative grid -->
      <div class="auth-layout__grid" aria-hidden="true"></div>

      <!-- Floating glow blobs -->
      <div class="auth-glow auth-glow--1" aria-hidden="true"></div>
      <div class="auth-glow auth-glow--2" aria-hidden="true"></div>

      <div class="auth-layout__branding" ref="brandingRef">
        <!-- Logo -->
        <div class="auth-anim auth-layout__logo-wrap">
          <div class="auth-layout__logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
              <defs>
                <linearGradient id="authBrainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#FF6B00" />
                  <stop offset="100%" stop-color="#FACC15" />
                </linearGradient>
                <linearGradient id="authFaceGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#00C6FF" />
                  <stop offset="100%" stop-color="#0072FF" />
                </linearGradient>
              </defs>
              <path d="M 50 10 L 70 15 L 88 35 L 90 55 L 78 78 L 60 88 L 50 84 L 40 88 L 22 78 L 10 55 L 12 35 L 30 15 Z" fill="none" stroke="url(#authBrainGrad)" stroke-width="4" stroke-linejoin="round" />
              <path d="M 50 10 V 25 M 50 84 V 70" fill="none" stroke="url(#authBrainGrad)" stroke-width="4" stroke-linecap="round" />
              <path d="M 30 15 L 40 25 V 35 M 70 15 L 60 25 V 35" fill="none" stroke="url(#authBrainGrad)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
              <path d="M 12 35 L 25 40 M 88 35 L 75 40" fill="none" stroke="url(#authBrainGrad)" stroke-width="3" stroke-linecap="round" />
              <path d="M 22 78 L 30 68 M 78 78 L 70 68" fill="none" stroke="url(#authBrainGrad)" stroke-width="3" stroke-linecap="round" />
              <rect x="30" y="42" width="8" height="8" rx="1.5" fill="url(#authFaceGrad)" />
              <rect x="62" y="42" width="8" height="8" rx="1.5" fill="url(#authFaceGrad)" />
              <path d="M 24 46 L 30 46 M 34 36 L 34 42 M 76 46 L 70 46 M 66 36 L 66 42" fill="none" stroke="url(#authFaceGrad)" stroke-width="2" stroke-linecap="round" />
              <circle cx="50" cy="46" r="1.5" fill="#CBD5E1" />
              <path d="M 38 46 L 48 46 M 52 46 L 62 46" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="2 2" />
              <path d="M 32 62 Q 50 78 68 58" fill="none" stroke="url(#authFaceGrad)" stroke-width="4.5" stroke-linecap="round" />
              <path d="M 60 56 L 68 58 L 66 66" fill="none" stroke="url(#authFaceGrad)" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </div>
        </div>

        <div class="auth-anim">
          <h1 class="auth-layout__title">TicketAI</h1>
          <p class="auth-layout__subtitle">
            Clasificación inteligente de tickets<br />con Naïve Bayes
          </p>
        </div>

        <!-- Mini live demo card -->
        <div class="auth-anim auth-demo">
          <div class="auth-demo__header">
            <span class="auth-demo__dot auth-demo__dot--green"></span>
            <span class="auth-demo__label">Clasificaciones recientes</span>
          </div>
          <div class="auth-demo__rows">
            <div
              v-for="(t, i) in demoTickets"
              :key="i"
              class="auth-demo__row"
            >
              <p class="auth-demo__row-text">{{ t.text }}</p>
              <div class="auth-demo__row-result">
                <span
                  class="auth-demo__badge"
                  :style="{ color: t.color, background: t.bg }"
                >{{ t.cat }}</span>
                <span class="auth-demo__pct">{{ t.pct }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature list -->
        <ul class="auth-anim auth-layout__features">
          <li
            v-for="(f, i) in features"
            :key="i"
            class="auth-layout__feature"
          >
            <component :is="f.icon" :size="14" class="auth-layout__feature-icon" />
            <span>{{ f.text }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- ─── Right panel ────────────────────────── -->
    <div class="auth-layout__right">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
/* ── Shell ───────────────────────────────────────────────── */
.auth-layout {
  display: flex;
  min-height: 100dvh;
}

/* ── Left panel ──────────────────────────────────────────── */
.auth-layout__left {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #04112b 0%, #0a1e47 45%, #0b2563 100%);
  color: #fff;
  padding: 56px 52px;
  overflow: hidden;
}

/* Subtle dot-grid overlay */
.auth-layout__grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}

/* Glow blobs */
.auth-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  pointer-events: none;
}

.auth-glow--1 {
  width: 400px;
  height: 400px;
  background: rgba(15, 98, 254, 0.35);
  top: -120px;
  right: -100px;
  animation: authFloat 10s ease-in-out infinite;
}

.auth-glow--2 {
  width: 280px;
  height: 280px;
  background: rgba(138, 63, 252, 0.25);
  bottom: -60px;
  left: -60px;
  animation: authFloat 13s ease-in-out infinite reverse;
}

@keyframes authFloat {
  0%, 100% { transform: translate(0, 0); }
  50%       { transform: translate(12px, -18px); }
}

/* ── Branding ────────────────────────────────────────────── */
.auth-layout__branding {
  position: relative;
  z-index: 1;
  max-width: 380px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}


.auth-layout__logo-wrap { display: flex; }

.auth-layout__logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  color: #fff;
}

.auth-layout__logo-icon svg {
  display: block;
}

.auth-layout__title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  margin-bottom: 8px;
}

.auth-layout__subtitle {
  font-size: 1rem;
  opacity: 0.65;
  line-height: 1.6;
}

/* ── Mini demo card ──────────────────────────────────────── */
.auth-demo {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 14px 16px;
  backdrop-filter: blur(8px);
}

.auth-demo__header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.auth-demo__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.auth-demo__dot--green {
  background: #34d399;
  box-shadow: 0 0 6px #34d399;
  animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

.auth-demo__label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.55;
}

.auth-demo__rows {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.auth-demo__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 10px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.auth-demo__row-text {
  font-size: 0.75rem;
  opacity: 0.75;
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.auth-demo__row-result {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.auth-demo__badge {
  font-size: 0.625rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
}

.auth-demo__pct {
  font-size: 0.6875rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  opacity: 0.7;
}

/* ── Feature list ────────────────────────────────────────── */
.auth-layout__features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.auth-layout__feature {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.8125rem;
  opacity: 0.75;
  line-height: 1.4;
}

.auth-layout__feature-icon {
  flex-shrink: 0;
  color: #60a5fa;
}

/* ── Right panel ─────────────────────────────────────────── */
.auth-layout__right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: var(--ds-surface);
  min-height: 100dvh;
}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 900px) {
  .auth-layout {
    flex-direction: column;
  }

  .auth-layout__left {
    padding: 36px 24px;
    min-height: auto;
  }

  .auth-demo { display: none; }

  .auth-layout__right {
    padding: 32px 20px;
    min-height: auto;
    align-items: flex-start;
  }
}

@media (prefers-reduced-motion: reduce) {
  .auth-glow--1,
  .auth-glow--2,
  .auth-demo__dot--green {
    animation: none;
  }
}
</style>
