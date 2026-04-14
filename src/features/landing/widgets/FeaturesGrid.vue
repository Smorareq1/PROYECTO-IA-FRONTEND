<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { animList, stagger, inView } from '@/core/composables/useMotionAnimate'
import { BrainCircuit, BarChart3, Shield, Zap, Target, Layers } from 'lucide-vue-next'

const features = [
  {
    icon: BrainCircuit,
    title: 'Naïve Bayes Classifier',
    description: 'Motor de clasificación basado en el teorema de Bayes con estimación de probabilidades por clase.',
    accent: '#0F62FE',
    tag: 'ML Core',
  },
  {
    icon: Zap,
    title: 'Clasificación Instantánea',
    description: 'Predicciones en menos de 50ms. El ticket se clasifica y enruta al departamento correcto al instante.',
    accent: '#F1C21B',
    tag: 'Performance',
  },
  {
    icon: BarChart3,
    title: 'Dashboard Analítico',
    description: 'Matriz de confusión interactiva, métricas por clase, y validación cruzada K-Fold en tiempo real.',
    accent: '#8A3FFC',
    tag: 'Analytics',
  },
  {
    icon: Target,
    title: 'Barras de Confianza',
    description: 'Visualiza la confianza del modelo en cada categoría. Transparencia total en las decisiones de la IA.',
    accent: '#198038',
    tag: 'Explainability',
  },
  {
    icon: Shield,
    title: 'Roles y Permisos',
    description: 'Sistema de roles (Cliente, Agente, Admin) con navegación y acciones adaptadas a cada perfil.',
    accent: '#DA1E28',
    tag: 'Security',
  },
  {
    icon: Layers,
    title: 'Preprocessing Pipeline',
    description: 'Tokenización, remoción de stopwords y stemming. Todo visible paso a paso en el Playground.',
    accent: '#EB6200',
    tag: 'NLP',
  },
]

const gridRef = ref<HTMLElement>()

onMounted(() => {
  if (!gridRef.value) return
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) return

  const easeOut = [0.22, 1, 0.36, 1] as const

  inView(
    gridRef.value,
    () => {
      const cards = gridRef.value!.querySelectorAll('.feature-card')
      animList(
        cards,
        { opacity: [0, 1], y: [32, 0] },
        { delay: stagger(0.09), duration: 0.5, easing: easeOut },
      )
    },
    { amount: 0.15 },
  )
})
</script>

<template>
  <section id="features" class="features">
    <div class="features__header">
      <span class="features__eyebrow">Características</span>
      <h2 class="features__title">Todo lo que necesitas</h2>
      <p class="features__subtitle">
        Un sistema completo de mesa de ayuda potenciado con inteligencia artificial
      </p>
    </div>

    <div class="features__grid" ref="gridRef">
      <article
        v-for="(feature, index) in features"
        :key="index"
        class="feature-card"
        :style="{ '--accent': feature.accent }"
      >
        <div class="feature-card__top">
          <div class="feature-card__icon-wrap">
            <component :is="feature.icon" :size="20" />
          </div>
          <span class="feature-card__tag">{{ feature.tag }}</span>
        </div>
        <h3 class="feature-card__title">{{ feature.title }}</h3>
        <p class="feature-card__description">{{ feature.description }}</p>
        <div class="feature-card__accent-line"></div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.features {
  padding: 96px 48px;
  max-width: 1320px;
  margin: 0 auto;
}

/* ── Header ──────────────────────────────────────────────── */
.features__header {
  text-align: center;
  margin-bottom: 64px;
}

.features__eyebrow {
  display: inline-block;
  font-size: var(--ds-text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--ds-primary-500);
  margin-bottom: 12px;
}

.features__title {
  font-size: var(--ds-text-4xl);
  font-weight: 800;
  color: var(--ds-text-primary);
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 14px;
}

.features__subtitle {
  font-size: var(--ds-text-lg);
  color: var(--ds-text-muted);
  max-width: 460px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ── Grid ────────────────────────────────────────────────── */
.features__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* ── Card ────────────────────────────────────────────────── */
.feature-card {
  position: relative;
  padding: 28px 24px 24px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  overflow: hidden;
  cursor: default;
  opacity: 0;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

:global(.dark .feature-card) {
  background: #18181B;
  border-color: #27272A;
}

.feature-card:hover {
  border-color: var(--ds-text-primary);
  box-shadow: 0 2px 0 var(--ds-text-primary);
  transform: translateY(-2px);
}

:global(.dark .feature-card:hover) {
  border-color: var(--ds-neutral-200);
  box-shadow: 0 2px 0 var(--ds-neutral-200);
}

/* Top accent line — grows on hover */
.feature-card__accent-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-card__accent-line {
  transform: scaleX(1);
}

.feature-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.feature-card__icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--ds-radius-sm);
  background: var(--ds-surface-raised);
  border: 1px solid var(--ds-border);
  color: var(--accent);
  transition: background 0.2s ease, border-color 0.2s ease;
}

:global(.dark .feature-card__icon-wrap) {
  background: #0F0F11;
  border-color: #27272A;
}

.feature-card:hover .feature-card__icon-wrap {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.feature-card__tag {
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 3px 8px;
  border-radius: var(--ds-radius-full);
  background: var(--ds-neutral-100);
  color: var(--ds-text-muted);
  border: 1px solid var(--ds-border);
}

:global(.dark .feature-card__tag) {
  background: #27272A;
  color: #A1A1AA;
  border-color: #3F3F46;
}

.feature-card__title {
  font-size: var(--ds-text-lg);
  font-weight: 700;
  color: var(--ds-text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.015em;
  line-height: 1.3;
}

.feature-card__description {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  line-height: 1.65;
}

/* ── Responsive ──────────────────────────────────────────── */
@media (max-width: 1024px) {
  .features {
    padding: 64px 24px;
  }
  .features__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .features {
    padding: 48px 16px;
  }
  .features__grid {
    grid-template-columns: 1fr;
  }
  .features__title {
    font-size: var(--ds-text-2xl);
  }
}

@media (prefers-reduced-motion: reduce) {
  .feature-card {
    opacity: 1;
    transition: none;
  }
  .feature-card__accent-line {
    transition: none;
  }
}
</style>
