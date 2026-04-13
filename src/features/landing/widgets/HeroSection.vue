<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { animEl, animList, stagger } from '@/core/composables/useMotionAnimate'
import { ArrowRight, BrainCircuit, Sparkles, Zap, Activity } from 'lucide-vue-next'

const heroRef   = ref<HTMLElement>()
const badgeRef  = ref<HTMLElement>()
const titleRef  = ref<HTMLElement>()
const descRef   = ref<HTMLElement>()
const actionsRef = ref<HTMLElement>()
const statsRef  = ref<HTMLElement>()
const cardRef   = ref<HTMLElement>()
const bar1Ref   = ref<HTMLElement>()
const bar2Ref   = ref<HTMLElement>()
const bar3Ref   = ref<HTMLElement>()

onMounted(() => {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const easeOut = [0.22, 1, 0.36, 1] as const

  if (!prefersReduced) {
    // Hide elements via JS before animating (progressive enhancement)
    const toHide = [badgeRef.value, titleRef.value, descRef.value, actionsRef.value, cardRef.value]
    toHide.forEach(el => { if (el) { el.style.opacity = '0' } })
    if (statsRef.value) {
      statsRef.value.querySelectorAll<HTMLElement>('.hero__stat, .hero__stat-divider')
        .forEach(el => { el.style.opacity = '0' })
    }

    requestAnimationFrame(() => {
      animEl(badgeRef.value,   { opacity: [0, 1], y: [-8, 0] }, { duration: 0.5, delay: 0.1,  easing: easeOut })
      animEl(titleRef.value,   { opacity: [0, 1], y: [28, 0] }, { duration: 0.6, delay: 0.2,  easing: easeOut })
      animEl(descRef.value,    { opacity: [0, 1], y: [20, 0] }, { duration: 0.5, delay: 0.35, easing: easeOut })
      animEl(actionsRef.value, { opacity: [0, 1], y: [16, 0] }, { duration: 0.5, delay: 0.45, easing: easeOut })
      animEl(cardRef.value,    { opacity: [0, 1], scale: [0.92, 1] }, { duration: 0.6, delay: 0.25, easing: easeOut })

      if (statsRef.value) {
        const items = statsRef.value.querySelectorAll('.hero__stat, .hero__stat-divider')
        animList(items, { opacity: [0, 1], y: [10, 0] }, { delay: stagger(0.08, { startDelay: 0.55 }), duration: 0.4, easing: easeOut })
      }
    })
  }

  /* — Animated progress bars (always run) — */
  const barDelay = prefersReduced ? 0 : 900
  setTimeout(() => {
    animEl(bar1Ref.value, { width: ['0%', '94%'] }, { duration: prefersReduced ? 0 : 1.2, easing: easeOut })
    animEl(bar2Ref.value, { width: ['0%', '3%']  }, { duration: prefersReduced ? 0 : 1.0, easing: easeOut })
    animEl(bar3Ref.value, { width: ['0%', '2%']  }, { duration: prefersReduced ? 0 : 0.9, easing: easeOut })
  }, barDelay)
})
</script>

<template>
  <section class="hero" ref="heroRef">
    <!-- Background -->
    <div class="hero__bg" aria-hidden="true">
      <div class="hero__grid"></div>
      <div class="hero__glow hero__glow--1"></div>
      <div class="hero__glow hero__glow--2"></div>
    </div>

    <!-- Left: Content -->
    <div class="hero__content">
      <div class="hero__badge" ref="badgeRef">
        <Sparkles :size="13" />
        <span>Clasificación con Naïve Bayes</span>
      </div>

      <h1 class="hero__title" ref="titleRef">
        Mesa de Ayuda<br />
        <span class="hero__title-accent">Inteligente</span>
      </h1>

      <p class="hero__description" ref="descRef">
        Clasifica automáticamente tickets de soporte usando inteligencia artificial.
        Enrutamiento instantáneo, métricas en tiempo real y análisis del modelo.
      </p>

      <div class="hero__actions" ref="actionsRef">
        <router-link to="/login" class="hero__btn hero__btn--primary">
          <span>Comenzar ahora</span>
          <ArrowRight :size="16" />
        </router-link>
        <a href="#features" class="hero__btn hero__btn--secondary">
          Ver características
        </a>
      </div>

      <div class="hero__stats" ref="statsRef">
        <div class="hero__stat">
          <span class="hero__stat-value">5</span>
          <span class="hero__stat-label">Categorías</span>
        </div>
        <div class="hero__stat-divider"></div>
        <div class="hero__stat">
          <span class="hero__stat-value">&lt;50ms</span>
          <span class="hero__stat-label">Clasificación</span>
        </div>
        <div class="hero__stat-divider"></div>
        <div class="hero__stat">
          <span class="hero__stat-value">K-Fold</span>
          <span class="hero__stat-label">Validación</span>
        </div>
      </div>
    </div>

    <!-- Right: Visual card -->
    <div class="hero__visual">
      <div class="hero__card" ref="cardRef">
        <div class="hero__card-header">
          <div class="hero__card-header-left">
            <div class="hero__card-icon-wrap">
              <BrainCircuit :size="16" />
            </div>
            <span>Análisis en tiempo real</span>
          </div>
          <div class="hero__card-live">
            <Activity :size="12" />
            <span>Live</span>
          </div>
        </div>

        <div class="hero__card-body">
          <div class="hero__card-input">
            <span class="hero__card-input-label">Ticket de entrada</span>
            <p>"Mi factura del mes pasado tiene un cargo duplicado que no reconozco."</p>
          </div>

          <div class="hero__card-result">
            <div class="hero__card-result-header">
              <span class="hero__card-badge hero__card-badge--facturacion">Facturación</span>
              <span class="hero__card-confidence">94.2%</span>
            </div>

            <div class="hero__card-bars">
              <div class="hero__bar">
                <div class="hero__bar-meta">
                  <span class="hero__bar-label">Facturación</span>
                  <span class="hero__bar-pct">94%</span>
                </div>
                <div class="hero__bar-track">
                  <div class="hero__bar-fill hero__bar-fill--facturacion" ref="bar1Ref" style="width:0%"></div>
                </div>
              </div>
              <div class="hero__bar">
                <div class="hero__bar-meta">
                  <span class="hero__bar-label">Consulta General</span>
                  <span class="hero__bar-pct">3%</span>
                </div>
                <div class="hero__bar-track">
                  <div class="hero__bar-fill hero__bar-fill--consulta" ref="bar2Ref" style="width:0%"></div>
                </div>
              </div>
              <div class="hero__bar">
                <div class="hero__bar-meta">
                  <span class="hero__bar-label">Queja</span>
                  <span class="hero__bar-pct">2%</span>
                </div>
                <div class="hero__bar-track">
                  <div class="hero__bar-fill hero__bar-fill--queja" ref="bar3Ref" style="width:0%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Floating pills -->
      <div class="hero__float hero__float--1" aria-hidden="true">
        <Zap :size="12" />
        <span>Tiempo real</span>
      </div>
      <div class="hero__float hero__float--2" aria-hidden="true">
        <Sparkles :size="12" />
        <span>NLP</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ── Layout ─────────────────────────────────────────────── */
.hero {
  position: relative;
  display: flex;
  align-items: center;
  gap: 72px;
  min-height: calc(100vh - 56px);
  padding: 64px 48px;
  max-width: 1320px;
  margin: 0 auto;
  overflow: hidden;
}

/* ── Background ─────────────────────────────────────────── */
.hero__bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--ds-neutral-100) 1px, transparent 1px),
    linear-gradient(90deg, var(--ds-neutral-100) 1px, transparent 1px);
  background-size: 56px 56px;
  opacity: 0.6;
  mask-image: radial-gradient(ellipse 80% 60% at 50% 40%, black 30%, transparent 80%);
}

:global(.dark .hero__grid) {
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  opacity: 0.5;
}

.hero__glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.hero__glow--1 {
  width: 580px;
  height: 580px;
  background: var(--ds-primary-500);
  opacity: 0.12;
  top: -180px;
  right: -80px;
  animation: floatSlow 9s ease-in-out infinite;
}

.hero__glow--2 {
  width: 360px;
  height: 360px;
  background: #8A3FFC;
  opacity: 0.1;
  bottom: -80px;
  left: -40px;
  animation: floatSlow 11s ease-in-out infinite reverse;
}

:global(.dark .hero__glow--1) { opacity: 0.18; }
:global(.dark .hero__glow--2) { opacity: 0.14; }

@keyframes floatSlow {
  0%, 100% { transform: translate(0, 0); }
  50%       { transform: translate(16px, -16px); }
}

/* ── Content ─────────────────────────────────────────────── */
.hero__content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 13px;
  background: var(--ds-primary-50);
  color: var(--ds-primary-700);
  border: 1px solid var(--ds-primary-200);
  border-radius: var(--ds-radius-full);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  margin-bottom: 20px;
}

:global(.dark .hero__badge) {
  background: rgba(96, 165, 250, 0.15);
  color: #93C5FD;
  border-color: rgba(96, 165, 250, 0.35);
}

.hero__title {
  font-size: clamp(2.25rem, 4vw, 3.75rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.04em;
  color: var(--ds-text-primary);
  margin-bottom: 20px;
}

.hero__title-accent {
  background: linear-gradient(135deg, var(--ds-primary-500) 0%, #8A3FFC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero__description {
  font-size: var(--ds-text-lg);
  color: var(--ds-text-secondary);
  max-width: 500px;
  line-height: 1.7;
  margin-bottom: 32px;
}

.hero__actions {
  display: flex;
  gap: 12px;
  margin-bottom: 48px;
}

.hero__btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 22px;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-base);
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.hero__btn--primary {
  background: var(--ds-primary-500);
  color: #fff;
  box-shadow: 0 1px 3px rgba(15, 98, 254, 0.3);
}

.hero__btn--primary:hover {
  background: var(--ds-primary-600);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(15, 98, 254, 0.35);
}

.hero__btn--primary:active { transform: translateY(0); }

.hero__btn--secondary {
  background: transparent;
  color: var(--ds-text-secondary);
  border: 1px solid var(--ds-border);
}

.hero__btn--secondary:hover {
  background: var(--ds-neutral-50);
  border-color: var(--ds-neutral-300);
  color: var(--ds-text-primary);
}

:global(.dark .hero__btn--secondary:hover) {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.2);
}

/* ── Stats ───────────────────────────────────────────────── */
.hero__stats {
  display: flex;
  align-items: center;
  gap: 24px;
}


.hero__stat-value {
  display: block;
  font-size: var(--ds-text-xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  font-family: var(--ds-font-mono);
  letter-spacing: -0.02em;
}

.hero__stat-label {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.hero__stat-divider {
  width: 1px;
  height: 32px;
  background: var(--ds-border);
}

/* ── Visual card ─────────────────────────────────────────── */
.hero__visual {
  flex: 1;
  position: relative;
  z-index: 1;
  max-width: 480px;
}

.hero__card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-xl);
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 24px 40px -8px rgba(0,0,0,0.12);
}

:global(.dark .hero__card) {
  background: #1C1C1F;
  border-color: #2E2E33;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.1),
    0 8px 40px rgba(0,0,0,0.7),
    0 0 80px -20px rgba(96, 165, 250, 0.15);
}

.hero__card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--ds-border);
  background: var(--ds-surface-raised);
}

:global(.dark .hero__card-header) {
  background: #222225;
  border-bottom-color: #2E2E33;
}

.hero__card-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.hero__card-icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--ds-radius-md);
  background: var(--ds-primary-50);
  color: var(--ds-primary-600);
}

:global(.dark .hero__card-icon-wrap) {
  background: rgba(96, 165, 250, 0.18);
  color: #60A5FA;
}

.hero__card-live {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 9px;
  border-radius: var(--ds-radius-full);
  background: rgba(25, 128, 56, 0.1);
  color: var(--ds-success);
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.hero__card-live svg {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

.hero__card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hero__card-input {
  background: var(--ds-neutral-50);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 12px 14px;
}

:global(.dark .hero__card-input) {
  background: #141416;
  border-color: #2E2E33;
}

.hero__card-input-label {
  display: block;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ds-text-muted);
  margin-bottom: 6px;
}

.hero__card-input p {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  font-style: italic;
  line-height: 1.5;
}

.hero__card-result {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hero__card-result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hero__card-badge {
  padding: 3px 10px;
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-weight: 600;
}

.hero__card-badge--facturacion {
  color: var(--ds-cat-facturacion);
  background: var(--ds-cat-facturacion-bg);
}

.hero__card-confidence {
  font-size: var(--ds-text-xl);
  font-weight: 700;
  font-family: var(--ds-font-mono);
  color: var(--ds-text-primary);
  letter-spacing: -0.03em;
}

/* ── Bars ────────────────────────────────────────────────── */
.hero__card-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hero__bar { display: flex; flex-direction: column; gap: 4px; }

.hero__bar-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hero__bar-label {
  font-size: 0.6875rem;
  color: var(--ds-text-muted);
  font-weight: 500;
}

.hero__bar-pct {
  font-size: 0.6875rem;
  font-family: var(--ds-font-mono);
  color: var(--ds-text-muted);
}

.hero__bar-track {
  height: 5px;
  background: var(--ds-neutral-100);
  border-radius: var(--ds-radius-full);
  overflow: hidden;
}

:global(.dark .hero__bar-track) {
  background: #27272A;
}

.hero__bar-fill {
  height: 100%;
  border-radius: var(--ds-radius-full);
  width: 0%;
}

.hero__bar-fill--facturacion { background: var(--ds-cat-facturacion); }
.hero__bar-fill--consulta    { background: var(--ds-cat-consulta); }
.hero__bar-fill--queja       { background: var(--ds-cat-queja); }

/* ── Floating pills ──────────────────────────────────────── */
.hero__float {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 13px;
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  color: var(--ds-text-primary);
  pointer-events: none;
}

:global(.dark .hero__float) {
  background: #1C1C1F;
  border-color: #2E2E33;
  box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08);
}

.hero__float svg { color: var(--ds-primary-500); }

.hero__float--1 {
  top: -14px;
  right: 32px;
  animation: float 3.2s ease-in-out infinite;
}

.hero__float--2 {
  bottom: 20px;
  left: -24px;
  animation: float 4s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-8px); }
}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 1024px) {
  .hero {
    flex-direction: column;
    padding: 48px 24px;
    gap: 48px;
    min-height: auto;
  }

  .hero__title {
    font-size: 2.5rem;
  }

  .hero__visual {
    max-width: 100%;
    width: 100%;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 32px 16px;
  }

  .hero__title {
    font-size: 2rem;
  }

  .hero__float {
    display: none;
  }

  .hero__stats {
    flex-wrap: wrap;
    gap: 16px;
  }

  .hero__actions {
    flex-direction: column;
  }

  .hero__btn {
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero__glow--1,
  .hero__glow--2,
  .hero__float--1,
  .hero__float--2,
  .hero__card-live svg {
    animation: none;
  }
}
</style>
