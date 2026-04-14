<script setup lang="ts">
import { computed } from 'vue'
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
  const rows: { value: [number, number, number]; itemStyle?: object }[] = []
  const n = props.data.labels.length
  props.data.matrix.forEach((row, i) => {
    row.forEach((val, j) => {
      const yFlipped = n - 1 - i
      const isDiagonal = i === j
      rows.push({
        value: [j, yFlipped, val],
        itemStyle: isDiagonal
          ? { borderColor: isDark.value ? '#60A5FA' : '#0F62FE', borderWidth: 2 }
          : undefined,
      })
    })
  })
  return rows
})

const maxVal = computed(() =>
  Math.max(...props.data.matrix.flat()),
)

const option = computed(() => ({
  backgroundColor: 'transparent',
  animation: true,
  animationDuration: 600,
  tooltip: {
    backgroundColor: isDark.value ? '#18181B' : '#FFFFFF',
    borderColor: isDark.value ? '#27272A' : '#E4E4E7',
    borderWidth: 1,
    textStyle: {
      color: isDark.value ? '#FAFAFA' : '#18181B',
      fontSize: 12,
    },
    extraCssText: 'border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);',
    formatter: (p: { data: { value: [number, number, number] } }) => {
      const [x, yFlipped, val] = p.data.value
      const y = props.data.labels.length - 1 - yFlipped
      const real = shortLabels.value[y]
      const pred = shortLabels.value[x]
      const isCorrect = y === x
      return `
        <div style="font-size:10px;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;color:${isCorrect ? '#198038' : '#DA1E28'};margin-bottom:6px;">
          ${isCorrect ? 'Correcto' : 'Error'}
        </div>
        <div style="display:grid;grid-template-columns:auto auto;gap:4px 12px;font-size:11px;">
          <span style="color:${isDark.value ? '#A1A1AA' : '#71717A'};">Real</span>
          <span style="font-weight:600;">${real}</span>
          <span style="color:${isDark.value ? '#A1A1AA' : '#71717A'};">Predicho</span>
          <span style="font-weight:600;">${pred}</span>
          <span style="color:${isDark.value ? '#A1A1AA' : '#71717A'};">Casos</span>
          <span style="font-weight:700;font-family:ui-monospace,monospace;">${val}</span>
        </div>
      `
    },
  },
  grid: { top: 16, bottom: 84, left: 110, right: 24 },
  xAxis: {
    type: 'category',
    data: shortLabels.value,
    name: 'Predicho →',
    nameLocation: 'middle',
    nameGap: 44,
    nameTextStyle: {
      color: isDark.value ? '#A1A1AA' : '#71717A',
      fontSize: 10,
      fontWeight: 700,
      letterSpacing: '0.08em',
    },
    axisLabel: {
      color: isDark.value ? '#A1A1AA' : '#52525B',
      fontSize: 10,
      rotate: 20,
      fontWeight: 500,
    },
    axisLine: { show: false },
    axisTick: { show: false },
    splitArea: { show: false },
  },
  yAxis: {
    type: 'category',
    data: [...shortLabels.value].reverse(),
    name: '↑ Real',
    nameLocation: 'middle',
    nameGap: 90,
    nameTextStyle: {
      color: isDark.value ? '#A1A1AA' : '#71717A',
      fontSize: 10,
      fontWeight: 700,
      letterSpacing: '0.08em',
    },
    axisLabel: {
      color: isDark.value ? '#A1A1AA' : '#52525B',
      fontSize: 10,
      fontWeight: 500,
    },
    axisLine: { show: false },
    axisTick: { show: false },
    splitArea: { show: false },
  },
  visualMap: {
    min: 0,
    max: maxVal.value,
    calculable: false,
    orient: 'horizontal',
    show: false,
    inRange: {
      color: isDark.value
        ? ['#0F0F11', '#1E40AF', '#0F62FE']
        : ['#FFFFFF', '#4A8BFF', '#0F62FE'],
    },
  },
  series: [{
    type: 'heatmap',
    data: heatmapData.value,
    label: {
      show: true,
      fontSize: 15,
      fontWeight: 800,
      fontFamily: 'ui-monospace, SFMono-Regular, monospace',
      formatter: (p: { data: { value: [number, number, number] } }) => {
        const val = p.data.value[2]
        return val === 0 ? '·' : String(val)
      },
      color: (p: { data: { value: [number, number, number] } }) => {
        const val = p.data.value[2]
        const ratio = val / (maxVal.value || 1)
        // In dark mode: always white — contrast is fine against the dark palette
        if (isDark.value) return '#FFFFFF'
        // In light mode: pure black below 40% of max, pure white above
        return ratio > 0.4 ? '#FFFFFF' : '#0A0A0A'
      },
      textBorderColor: 'transparent',
      textShadowBlur: 0,
    },
    itemStyle: {
      borderRadius: 2,
      borderColor: isDark.value ? '#0F0F11' : '#FFFFFF',
      borderWidth: 3,
    },
    emphasis: {
      itemStyle: {
        shadowBlur: 0,
        borderColor: isDark.value ? '#60A5FA' : '#0F62FE',
        borderWidth: 3,
      },
    },
  }],
}))
</script>

<template>
  <div class="cm-wrap">
    <VChart :option="option" autoresize style="height: 360px;" />
    <div class="cm-legend">
      <div class="cm-legend__item">
        <span class="cm-legend__swatch cm-legend__swatch--diag"></span>
        <span>Aciertos (diagonal)</span>
      </div>
      <div class="cm-legend__scale">
        <span class="cm-legend__label">0</span>
        <div class="cm-legend__gradient"></div>
        <span class="cm-legend__label">{{ maxVal }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cm-wrap {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  padding: 18px;
}

:global(.dark .cm-wrap) { background: #18181B; border-color: #27272A; }

.cm-legend {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-top: 12px;
  margin-top: 8px;
  border-top: 1px dashed var(--ds-border);
  font-size: 0.6875rem;
  color: var(--ds-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
  flex-wrap: wrap;
}

:global(.dark .cm-legend) { border-top-color: #27272A; }

.cm-legend__item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.cm-legend__swatch {
  width: 14px;
  height: 14px;
  border-radius: 2px;
}

.cm-legend__swatch--diag {
  background: var(--ds-primary-500);
  border: 2px solid var(--ds-primary-500);
}

.cm-legend__scale {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.cm-legend__gradient {
  width: 120px;
  height: 8px;
  border-radius: 2px;
  background: linear-gradient(to right, #FFFFFF, #4A8BFF, #0F62FE);
  border: 1px solid var(--ds-border);
}

:global(.dark .cm-legend__gradient) {
  background: linear-gradient(to right, #0F0F11, #1E40AF, #0F62FE);
  border-color: #27272A;
}

.cm-legend__label {
  font-family: var(--ds-font-mono);
  color: var(--ds-text-primary);
}
</style>
