<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import type { ClassMetrics } from '../models/metrics'
import { CATEGORY_LABELS } from '@/core/config/constants'
import { useTheme } from '@/core/composables/useTheme'

use([CanvasRenderer, PieChart, TooltipComponent, LegendComponent])

const props = defineProps<{ metrics: ClassMetrics[] }>()
const { isDark } = useTheme()

const COLORS: Record<string, string> = {
  soporte_tecnico:  '#0F62FE',
  facturacion:      '#8A3FFC',
  consulta_general: '#009D9A',
  queja:            '#DA1E28',
  cancelacion:      '#EB6200',
}

const option = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    formatter: (p: { name: string; value: number; percent: number }) =>
      `${p.name}: ${p.value} muestras (${p.percent?.toFixed(1)}%)`,
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center',
    textStyle: { color: isDark.value ? '#A1A1AA' : '#71717A', fontSize: 11 },
  },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    center: ['38%', '50%'],
    data: props.metrics.map(m => ({
      name: CATEGORY_LABELS[m.class],
      value: m.support,
      itemStyle: { color: COLORS[m.class] ?? '#999' },
    })),
    label: {
      show: true,
      formatter: '{d}%',
      color: isDark.value ? '#A1A1AA' : '#71717A',
      fontSize: 10,
    },
    emphasis: {
      itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.3)' },
    },
  }],
}))
</script>

<template>
  <div class="cat-dist">
    <VChart :option="option" autoresize style="height: 260px;" />
  </div>
</template>

<style scoped>
.cat-dist {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 16px;
}

:global(.dark .cat-dist) { background: #18181B; border-color: #27272A; }
</style>
