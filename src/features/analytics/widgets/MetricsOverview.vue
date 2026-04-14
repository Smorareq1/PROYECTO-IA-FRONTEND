<script setup lang="ts">
import { computed } from 'vue'
import { Target, Gauge, Ticket, Timer } from 'lucide-vue-next'
import StatCard from '@/design-system/molecules/StatCard.vue'
import type { ModelMetrics } from '../models/metrics'
import type { ModelInfo } from '../models/metrics'

const props = defineProps<{
  metrics: ModelMetrics
  modelInfo: ModelInfo | null
}>()

const cards = computed(() => [
  {
    title: 'Accuracy global',
    value: `${(props.metrics.accuracy * 100).toFixed(1)}%`,
    subtitle: 'sobre el conjunto de test',
    icon: Target,
    variant: 'primary' as const,
  },
  {
    title: 'Macro F1-Score',
    value: `${(props.metrics.macro_f1 * 100).toFixed(1)}%`,
    subtitle: 'promedio de todas las clases',
    icon: Gauge,
    variant: 'success' as const,
  },
  {
    title: 'Documentos entrenados',
    value: props.modelInfo?.doc_count?.toLocaleString() ?? '—',
    subtitle: 'en el dataset de entrenamiento',
    icon: Ticket,
    variant: 'default' as const,
  },
  {
    title: 'Tamaño del vocabulario',
    value: props.modelInfo?.vocab_size?.toLocaleString() ?? '—',
    subtitle: 'palabras únicas (post-stem)',
    icon: Timer,
    variant: 'default' as const,
  },
])
</script>

<template>
  <div class="metrics-grid">
    <StatCard
      v-for="card in cards"
      :key="card.title"
      :title="card.title"
      :value="card.value"
      :subtitle="card.subtitle"
      :icon="card.icon"
      :variant="card.variant"
    />
  </div>
</template>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}
</style>
