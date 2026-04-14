<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  MarkLineComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import type { KFoldReport } from '../models/kfold'
import { useTheme } from '@/core/composables/useTheme'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, MarkLineComponent])

const props = defineProps<{ data: KFoldReport }>()
const { isDark } = useTheme()

const axisColor = computed(() => isDark.value ? '#52525B' : '#D4D4D8')
const labelColor = computed(() => isDark.value ? '#A1A1AA' : '#71717A')

const option = computed(() => ({
  backgroundColor: 'transparent',
  tooltip: {
    trigger: 'axis',
    formatter: (params: { axisValue: string; seriesName: string; value: number }[]) =>
      `<b>Fold ${params[0]?.axisValue}</b><br/>` +
      params.map(p => `${p.seriesName}: ${(p.value * 100).toFixed(2)}%`).join('<br/>'),
  },
  legend: {
    data: ['Accuracy', 'Macro F1'],
    textStyle: { color: labelColor.value, fontSize: 12 },
    bottom: 0,
  },
  grid: { top: 16, left: 52, right: 24, bottom: 44 },
  xAxis: {
    type: 'category',
    data: props.data.folds.map(f => String(f.fold)),
    name: 'Fold',
    nameLocation: 'middle',
    nameGap: 28,
    axisLine: { lineStyle: { color: axisColor.value } },
    axisLabel: { color: labelColor.value },
  },
  yAxis: {
    type: 'value',
    min: 0.5,
    max: 1,
    axisLine: { lineStyle: { color: axisColor.value } },
    splitLine: { lineStyle: { color: axisColor.value, type: 'dashed' } },
    axisLabel: {
      color: labelColor.value,
      formatter: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
  },
  series: [
    {
      name: 'Accuracy',
      type: 'line',
      data: props.data.folds.map(f => f.accuracy),
      smooth: true,
      symbol: 'circle',
      symbolSize: 7,
      lineStyle: { color: '#0F62FE', width: 2 },
      itemStyle: { color: '#0F62FE' },
      markLine: {
        silent: true,
        data: [{ yAxis: props.data.mean.accuracy, name: 'Mean Acc' }],
        lineStyle: { color: '#0F62FE', type: 'dashed', opacity: 0.5 },
        label: { show: false },
      },
    },
    {
      name: 'Macro F1',
      type: 'line',
      data: props.data.folds.map(f => f.macro_f1),
      smooth: true,
      symbol: 'circle',
      symbolSize: 7,
      lineStyle: { color: '#009D9A', width: 2 },
      itemStyle: { color: '#009D9A' },
      markLine: {
        silent: true,
        data: [{ yAxis: props.data.mean.macro_f1, name: 'Mean F1' }],
        lineStyle: { color: '#009D9A', type: 'dashed', opacity: 0.5 },
        label: { show: false },
      },
    },
  ],
}))
</script>

<template>
  <div class="kfold-chart">
    <VChart :option="option" autoresize style="height: 280px;" />
  </div>
</template>

<style scoped>
.kfold-chart {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 16px;
}

:global(.dark .kfold-chart) { background: #18181B; border-color: #27272A; }
</style>
