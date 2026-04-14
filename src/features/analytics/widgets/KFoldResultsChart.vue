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
  MarkAreaComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import type { KFoldReport } from '../models/kfold'
import { useTheme } from '@/core/composables/useTheme'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, MarkLineComponent, MarkAreaComponent])

const props = defineProps<{ data: KFoldReport }>()
const { isDark } = useTheme()

const axisColor  = computed(() => isDark.value ? '#3F3F46' : '#E4E4E7')
const labelColor = computed(() => isDark.value ? '#A1A1AA' : '#52525B')
const gridLine   = computed(() => isDark.value ? '#27272A' : '#F4F4F5')

/* Primary: --ds-primary-500 (#0F62FE) — editorial blue
   Secondary: strong teal-green (not pastel) */
const PRIMARY = '#0F62FE'
const SECONDARY = '#007D79'

const option = computed(() => ({
  backgroundColor: 'transparent',
  animation: true,
  animationDuration: 700,
  animationEasing: 'cubicOut',
  tooltip: {
    trigger: 'axis',
    backgroundColor: isDark.value ? '#18181B' : '#FFFFFF',
    borderColor: isDark.value ? '#27272A' : '#E4E4E7',
    borderWidth: 1,
    textStyle: {
      color: isDark.value ? '#FAFAFA' : '#18181B',
      fontSize: 12,
    },
    extraCssText: 'border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);',
    formatter: (params: { axisValue: string; seriesName: string; value: number; color: string }[]) =>
      `<div style="font-weight:700;margin-bottom:6px;letter-spacing:0.04em;text-transform:uppercase;font-size:10px;">Fold ${params[0]?.axisValue}</div>` +
      params.map(p =>
        `<div style="display:flex;align-items:center;gap:8px;font-family:ui-monospace,SFMono-Regular,monospace;">
          <span style="width:8px;height:8px;background:${p.color};border-radius:50%;"></span>
          <span>${p.seriesName}</span>
          <span style="margin-left:auto;font-weight:700;">${(p.value * 100).toFixed(2)}%</span>
         </div>`,
      ).join(''),
  },
  legend: {
    data: ['Accuracy', 'Macro F1'],
    textStyle: {
      color: labelColor.value,
      fontSize: 11,
      fontWeight: 600,
    },
    bottom: 0,
    icon: 'roundRect',
    itemWidth: 14,
    itemHeight: 4,
    itemGap: 20,
  },
  grid: { top: 24, left: 54, right: 24, bottom: 44 },
  xAxis: {
    type: 'category',
    data: props.data.folds.map(f => String(f.fold)),
    name: 'Fold',
    nameLocation: 'middle',
    nameGap: 28,
    nameTextStyle: {
      color: labelColor.value,
      fontSize: 10,
      fontWeight: 600,
    },
    axisLine: { lineStyle: { color: axisColor.value } },
    axisTick: { show: false },
    axisLabel: {
      color: labelColor.value,
      fontSize: 11,
      fontFamily: 'ui-monospace, SFMono-Regular, monospace',
    },
  },
  yAxis: {
    type: 'value',
    min: 0.5,
    max: 1,
    axisLine: { show: false },
    axisTick: { show: false },
    splitLine: { lineStyle: { color: gridLine.value, type: 'solid' } },
    axisLabel: {
      color: labelColor.value,
      fontSize: 11,
      fontFamily: 'ui-monospace, SFMono-Regular, monospace',
      formatter: (v: number) => `${(v * 100).toFixed(0)}%`,
    },
  },
  series: [
    {
      name: 'Accuracy',
      type: 'line',
      data: props.data.folds.map(f => f.accuracy),
      smooth: false,
      symbol: 'circle',
      symbolSize: 14,
      showSymbol: true,
      lineStyle: { color: PRIMARY, width: 3 },
      itemStyle: {
        color: PRIMARY,
        borderColor: isDark.value ? '#0F0F11' : '#FFFFFF',
        borderWidth: 3,
      },
      label: {
        show: true,
        position: 'top',
        distance: 10,
        color: PRIMARY,
        fontSize: 11,
        fontWeight: 800,
        fontFamily: 'ui-monospace, SFMono-Regular, monospace',
        backgroundColor: isDark.value ? '#18181B' : '#FFFFFF',
        borderColor: PRIMARY,
        borderWidth: 1,
        borderRadius: 3,
        padding: [3, 6],
        formatter: (p: { value: number }) => `${(p.value * 100).toFixed(1)}%`,
      },
      emphasis: {
        scale: 1.3,
        itemStyle: { color: PRIMARY, borderColor: PRIMARY },
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: isDark.value ? 'rgba(15,98,254,0.28)' : 'rgba(15,98,254,0.18)' },
            { offset: 1, color: 'rgba(15,98,254,0)' },
          ],
        },
      },
      markLine: {
        silent: true,
        symbol: 'none',
        data: [{ yAxis: props.data.mean.accuracy, name: 'μ Acc' }],
        lineStyle: { color: PRIMARY, type: [4, 4], opacity: 0.5, width: 1.2 },
        label: {
          show: true,
          position: 'insideEndTop',
          color: PRIMARY,
          fontSize: 10,
          fontWeight: 700,
          fontFamily: 'ui-monospace, SFMono-Regular, monospace',
          formatter: `μ ${(props.data.mean.accuracy * 100).toFixed(1)}%`,
        },
      },
    },
    {
      name: 'Macro F1',
      type: 'line',
      data: props.data.folds.map(f => f.macro_f1),
      smooth: false,
      symbol: 'rect',
      symbolSize: 12,
      showSymbol: true,
      lineStyle: { color: SECONDARY, width: 3 },
      itemStyle: {
        color: SECONDARY,
        borderColor: isDark.value ? '#0F0F11' : '#FFFFFF',
        borderWidth: 3,
      },
      label: {
        show: true,
        position: 'bottom',
        distance: 10,
        color: SECONDARY,
        fontSize: 11,
        fontWeight: 800,
        fontFamily: 'ui-monospace, SFMono-Regular, monospace',
        backgroundColor: isDark.value ? '#18181B' : '#FFFFFF',
        borderColor: SECONDARY,
        borderWidth: 1,
        borderRadius: 3,
        padding: [3, 6],
        formatter: (p: { value: number }) => `${(p.value * 100).toFixed(1)}%`,
      },
      emphasis: {
        scale: 1.3,
        itemStyle: { color: SECONDARY, borderColor: SECONDARY },
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: isDark.value ? 'rgba(0,125,121,0.24)' : 'rgba(0,125,121,0.14)' },
            { offset: 1, color: 'rgba(0,125,121,0)' },
          ],
        },
      },
      markLine: {
        silent: true,
        symbol: 'none',
        data: [{ yAxis: props.data.mean.macro_f1, name: 'μ F1' }],
        lineStyle: { color: SECONDARY, type: [4, 4], opacity: 0.5, width: 1.2 },
        label: {
          show: true,
          position: 'insideEndBottom',
          color: SECONDARY,
          fontSize: 10,
          fontWeight: 700,
          fontFamily: 'ui-monospace, SFMono-Regular, monospace',
          formatter: `μ ${(props.data.mean.macro_f1 * 100).toFixed(1)}%`,
        },
      },
    },
  ],
}))
</script>

<template>
  <div class="kfold-chart">
    <VChart :option="option" autoresize style="height: 300px;" />
  </div>
</template>

<style scoped>
.kfold-chart {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  padding: 18px;
}

:global(.dark .kfold-chart) { background: #18181B; border-color: #27272A; }
</style>
