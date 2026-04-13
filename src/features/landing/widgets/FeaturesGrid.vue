<script setup lang="ts">
import { BrainCircuit, BarChart3, Shield, Zap, Target, Layers } from 'lucide-vue-next'

const features = [
  {
    icon: BrainCircuit,
    title: 'Naïve Bayes Classifier',
    description: 'Motor de clasificación basado en el teorema de Bayes con estimación de probabilidades por clase.',
    accent: 'var(--ds-primary-500)',
  },
  {
    icon: Zap,
    title: 'Clasificación Instantánea',
    description: 'Predicciones en menos de 50ms. El ticket se clasifica y enruta al departamento correcto al instante.',
    accent: 'var(--ds-warning)',
  },
  {
    icon: BarChart3,
    title: 'Dashboard Analítico',
    description: 'Matriz de confusión interactiva, métricas por clase, y validación cruzada K-Fold en tiempo real.',
    accent: 'var(--ds-cat-facturacion)',
  },
  {
    icon: Target,
    title: 'Barras de Confianza',
    description: 'Visualiza la confianza del modelo en cada categoría. Transparencia total en las decisiones de la IA.',
    accent: 'var(--ds-success)',
  },
  {
    icon: Shield,
    title: 'Roles y Permisos',
    description: 'Sistema de roles (Cliente, Agente, Admin) con navegación y acciones adaptadas a cada perfil.',
    accent: 'var(--ds-danger)',
  },
  {
    icon: Layers,
    title: 'Preprocessing Pipeline',
    description: 'Tokenización, remoción de stopwords y stemming. Todo visible paso a paso en el Playground.',
    accent: 'var(--ds-cat-cancelacion)',
  },
]
</script>

<template>
  <section id="features" class="features">
    <div class="features__header">
      <span class="features__label">Características</span>
      <h2 class="features__title">Todo lo que necesitas</h2>
      <p class="features__subtitle">
        Un sistema completo de mesa de ayuda potenciado con inteligencia artificial
      </p>
    </div>

    <div class="features__grid">
      <div
        v-for="(feature, index) in features"
        :key="index"
        class="feature-card"
        :style="{ '--accent': feature.accent, animationDelay: `${index * 0.1}s` }"
      >
        <div class="feature-card__icon">
          <component :is="feature.icon" :size="22" />
        </div>
        <h3 class="feature-card__title">{{ feature.title }}</h3>
        <p class="feature-card__description">{{ feature.description }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.features {
  padding: 96px 48px;
  max-width: 1320px;
  margin: 0 auto;
}

.features__header {
  text-align: center;
  margin-bottom: 64px;
}

.features__label {
  display: inline-block;
  font-size: var(--ds-text-xs);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--ds-primary-500);
  margin-bottom: 12px;
}

.features__title {
  font-size: var(--ds-text-4xl);
  font-weight: 800;
  color: var(--ds-text-primary);
  letter-spacing: -0.03em;
  margin-bottom: 12px;
}

.features__subtitle {
  font-size: var(--ds-text-lg);
  color: var(--ds-text-muted);
  max-width: 480px;
  margin: 0 auto;
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  padding: 32px 28px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-xl);
  background: var(--ds-surface);
  transition: all 0.25s ease;
  animation: slideUp 0.5s ease-out both;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  border-color: var(--ds-neutral-300);
  box-shadow: var(--ds-shadow-md);
  transform: translateY(-4px);
}

.feature-card__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--ds-radius-lg);
  background: var(--ds-neutral-50);
  color: var(--accent, var(--ds-primary-500));
  margin-bottom: 16px;
}

.feature-card__title {
  font-size: var(--ds-text-lg);
  font-weight: 700;
  color: var(--ds-text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.feature-card__description {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  line-height: 1.6;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 1024px) {
  .features__grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .features {
    padding: 64px 24px;
  }
}

@media (max-width: 640px) {
  .features__grid {
    grid-template-columns: 1fr;
  }
  .features__title {
    font-size: var(--ds-text-2xl);
  }
}
</style>
