<script setup lang="ts">
import { computed, ref, watchEffect } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { HeatmapChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  VisualMapComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import type { ConfusionMatrix as CMType } from '../models/metrics'
import { CATEGORY_LABELS } from '@/core/config/constants'
import { useTheme } from '@/core/composables/useTheme'

use([CanvasRenderer, HeatmapChart, GridComponent, TooltipComponent, VisualMapComponent])

const props = defineProps<{ data: CMType }>()
const { isDark } = useTheme()

const shortLabels = computed(() =>
  props.data.labels.map(l => CATEGORY_LABELS[l] ?? l),
)

const heatmapData = computed(() => {
  const rows: [number, number, number][] = []
  props.data.matrix.forEach((row, i) => {
    row.forEach((val, j) => {
      rows.push([j, props.data.labels.length - 1 - i, val])
    })
  })
  return rows
})

const maxVal = computed(() =>
  Math.max(...props.data.matrix.flat()),
)

const option = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    formatter: (p: { data: [number, number, number] }) => {
      const [x, yFlipped, val] = p.data
      const y = props.data.labels.length - 1 - yFlipped
      const real = shortLabels.value[y]
      const pred = shortLabels.value[x]
      return `<b>Real:</b> ${real}<br/><b>Predicho:</b> ${pred}<br/><b>Casos:</b> ${val}`
    },
  },
  grid: { top: 10, bottom: 80, left: 100, right: 60 },
  xAxis: {
    type: 'category',
    data: shortLabels.value,
    name: 'Predicho',
    nameLocation: 'middle',
    nameGap: 32,
    axisLabel: {
      color: isDark.value ? '#A1A1AA' : '#71717A',
      fontSize: 10,
      rotate: 20,
    },
    axisLine: { lineStyle: { color: isDark.value ? '#27272A' : '#E4E4E7' } },
  },
  yAxis: {
    type: 'category',
    data: [...shortLabels.value].reverse(),
    name: 'Real',
    nameLocation: 'middle',
    nameGap: 80,
    axisLabel: {
      color: isDark.value ? '#A1A1AA' : '#71717A',
      fontSize: 10,
    },
    axisLine: { lineStyle: { color: isDark.value ? '#27272A' : '#E4E4E7' } },
  },
  visualMap: {
    min: 0,
    max: maxVal.value,
    calculable: false,
    orient: 'horizontal',
    show: false,
    inRange: {
      color: isDark.value
        ? ['#1e3a5f', '#0F62FE']
        : ['#EDF5FF', '#0F62FE'],
    },
  },
  series: [{
    type: 'heatmap',
    data: heatmapData.value,
    label: {
      show: true,
      color: isDark.value ? '#fff' : '#161616',
      fontSize: 12,
      fontWeight: 600,
    },
    emphasis: {
      itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.3)' },
    },
  }],
}))
</script>

<template>
  <div class="cm-wrap">
    <VChart :option="option" autoresize style="height: 340px;" />
  </div>
</template>

<style scoped>
.cm-wrap {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 16px;
}

:global(.dark .cm-wrap) { background: #18181B; border-color: #27272A; }
</style>
