<script setup lang="ts">
import { ArrowRight, BrainCircuit, Sparkles, Zap } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <section class="hero">
    <div class="hero__bg">
      <div class="hero__grid"></div>
      <div class="hero__glow hero__glow--1"></div>
      <div class="hero__glow hero__glow--2"></div>
    </div>

    <div class="hero__content">
      <div class="hero__badge">
        <Sparkles :size="14" />
        <span>Clasificación con Naïve Bayes</span>
      </div>

      <h1 class="hero__title">
        Mesa de Ayuda<br />
        <span class="hero__title-accent">Inteligente</span>
      </h1>

      <p class="hero__description">
        Clasifica automáticamente tickets de soporte usando inteligencia artificial.
        Enrutamiento instantáneo, métricas en tiempo real y análisis del modelo.
      </p>

      <div class="hero__actions">
        <router-link to="/login" class="hero__btn hero__btn--primary">
          <span>Comenzar</span>
          <ArrowRight :size="18" />
        </router-link>
        <a href="#features" class="hero__btn hero__btn--secondary">
          Ver características
        </a>
      </div>

      <div class="hero__stats">
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

    <div class="hero__visual">
      <div class="hero__card hero__card--main">
        <div class="hero__card-header">
          <BrainCircuit :size="20" />
          <span>Predicción</span>
        </div>
        <div class="hero__card-body">
          <div class="hero__card-input">
            "Mi factura del mes pasado tiene un cargo duplicado..."
          </div>
          <div class="hero__card-result">
            <div class="hero__card-category">
              <span class="hero__card-badge hero__card-badge--facturacion">Facturación</span>
              <span class="hero__card-confidence">94.2%</span>
            </div>
            <div class="hero__card-bars">
              <div class="hero__bar">
                <span class="hero__bar-label">Facturación</span>
                <div class="hero__bar-track">
                  <div class="hero__bar-fill hero__bar-fill--facturacion" style="width: 94%"></div>
                </div>
              </div>
              <div class="hero__bar">
                <span class="hero__bar-label">Consulta General</span>
                <div class="hero__bar-track">
                  <div class="hero__bar-fill hero__bar-fill--consulta" style="width: 3%"></div>
                </div>
              </div>
              <div class="hero__bar">
                <span class="hero__bar-label">Queja</span>
                <div class="hero__bar-track">
                  <div class="hero__bar-fill hero__bar-fill--queja" style="width: 2%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Floating badges -->
      <div class="hero__float hero__float--1">
        <Zap :size="14" />
        <span>Tiempo real</span>
      </div>
      <div class="hero__float hero__float--2">
        <Sparkles :size="14" />
        <span>NLP</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  display: flex;
  align-items: center;
  gap: 64px;
  min-height: calc(100vh - 56px);
  padding: 64px 48px;
  max-width: 1320px;
  margin: 0 auto;
  overflow: hidden;
}

/* Background effects */
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
  background-size: 64px 64px;
  opacity: 0.5;
  mask-image: radial-gradient(ellipse 80% 60% at 50% 40%, black 30%, transparent 80%);
}

:global(.dark) .hero__grid {
  background-image:
    linear-gradient(var(--ds-neutral-200) 1px, transparent 1px),
    linear-gradient(90deg, var(--ds-neutral-200) 1px, transparent 1px);
  opacity: 0.3;
}

.hero__glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}

.hero__glow--1 {
  width: 600px;
  height: 600px;
  background: var(--ds-primary-500);
  top: -200px;
  right: -100px;
  animation: floatSlow 8s ease-in-out infinite;
}

.hero__glow--2 {
  width: 400px;
  height: 400px;
  background: #8A3FFC;
  bottom: -100px;
  left: -50px;
  animation: floatSlow 10s ease-in-out infinite reverse;
}

@keyframes floatSlow {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -20px); }
}

/* Content */
.hero__content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: var(--ds-primary-50);
  color: var(--ds-primary-700);
  border: 1px solid var(--ds-primary-200);
  border-radius: var(--ds-radius-full);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  margin-bottom: 24px;
  animation: slideDown 0.5s ease-out;
}

.hero__title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.04em;
  color: var(--ds-text-primary);
  margin-bottom: 20px;
  animation: slideUp 0.6s ease-out;
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
  max-width: 520px;
  line-height: 1.7;
  margin-bottom: 32px;
  animation: slideUp 0.7s ease-out;
}

.hero__actions {
  display: flex;
  gap: 12px;
  margin-bottom: 48px;
  animation: slideUp 0.8s ease-out;
}

.hero__btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
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
}

.hero__btn--primary:hover {
  background: var(--ds-primary-600);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(15, 98, 254, 0.35);
}

.hero__btn--secondary {
  background: transparent;
  color: var(--ds-text-secondary);
  border: 1px solid var(--ds-border);
}

.hero__btn--secondary:hover {
  background: var(--ds-neutral-50);
  border-color: var(--ds-neutral-300);
}

/* Stats */
.hero__stats {
  display: flex;
  align-items: center;
  gap: 24px;
  animation: fadeIn 1s ease-out;
}

.hero__stat-value {
  display: block;
  font-size: var(--ds-text-xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  font-family: var(--ds-font-mono);
}

.hero__stat-label {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.hero__stat-divider {
  width: 1px;
  height: 36px;
  background: var(--ds-border);
}

/* Visual card */
.hero__visual {
  flex: 1;
  position: relative;
  z-index: 1;
  animation: scaleIn 0.8s ease-out;
}

.hero__card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-xl);
  overflow: hidden;
  box-shadow: var(--ds-shadow-lg);
}

.hero__card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  border-bottom: 1px solid var(--ds-border);
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.hero__card-header svg {
  color: var(--ds-primary-500);
}

.hero__card-body {
  padding: 20px;
}

.hero__card-input {
  background: var(--ds-neutral-50);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  padding: 14px 16px;
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  font-style: italic;
  margin-bottom: 20px;
  line-height: 1.5;
}

.hero__card-category {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.hero__card-badge {
  padding: 4px 12px;
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-weight: 600;
}

.hero__card-badge--facturacion {
  color: var(--ds-cat-facturacion);
  background: var(--ds-cat-facturacion-bg);
}

.hero__card-confidence {
  font-size: var(--ds-text-lg);
  font-weight: 700;
  font-family: var(--ds-font-mono);
  color: var(--ds-text-primary);
}

.hero__card-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.hero__bar {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hero__bar-label {
  font-size: 0.6875rem;
  color: var(--ds-text-muted);
}

.hero__bar-track {
  height: 6px;
  background: var(--ds-neutral-100);
  border-radius: var(--ds-radius-full);
  overflow: hidden;
}

.hero__bar-fill {
  height: 100%;
  border-radius: var(--ds-radius-full);
  transition: width 1.5s ease-out;
}

.hero__bar-fill--facturacion { background: var(--ds-cat-facturacion); }
.hero__bar-fill--consulta    { background: var(--ds-cat-consulta); }
.hero__bar-fill--queja       { background: var(--ds-cat-queja); }

/* Floating badges */
.hero__float {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  box-shadow: var(--ds-shadow-md);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.hero__float svg {
  color: var(--ds-primary-500);
}

.hero__float--1 {
  top: -12px;
  right: 40px;
  animation: float 3s ease-in-out infinite;
}

.hero__float--2 {
  bottom: 24px;
  left: -20px;
  animation: float 4s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@media (max-width: 1024px) {
  .hero {
    flex-direction: column;
    padding: 40px 24px;
    gap: 40px;
    min-height: auto;
  }

  .hero__title {
    font-size: 2.5rem;
  }

  .hero__visual {
    max-width: 500px;
    width: 100%;
  }
}

@media (max-width: 640px) {
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
}
</style>
