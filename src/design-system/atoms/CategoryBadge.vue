<script setup lang="ts">
import { computed } from 'vue'
import type { Category } from '@/core/config/constants'
import { CATEGORY_LABELS } from '@/core/config/constants'

interface Props {
  category: Category
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
})

const label = computed(() => CATEGORY_LABELS[props.category] || props.category)
</script>

<template>
  <span
    class="category-badge"
    :class="[`category-badge--${category}`, `category-badge--${size}`]"
  >
    {{ label }}
  </span>
</template>

<style scoped>
.category-badge {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
  border-radius: var(--ds-radius-sm);
  white-space: nowrap;
  transition: all 0.15s ease;
}

/* Sizes */
.category-badge--sm {
  font-size: 0.6875rem;
  padding: 2px 8px;
  letter-spacing: 0.01em;
}

.category-badge--md {
  font-size: var(--ds-text-xs);
  padding: 4px 10px;
}

.category-badge--lg {
  font-size: var(--ds-text-sm);
  padding: 6px 14px;
}

/* Category colors */
.category-badge--soporte_tecnico {
  color: var(--ds-cat-soporte);
  background: var(--ds-cat-soporte-bg);
}

.category-badge--facturacion {
  color: var(--ds-cat-facturacion);
  background: var(--ds-cat-facturacion-bg);
}

.category-badge--consulta_general {
  color: var(--ds-cat-consulta);
  background: var(--ds-cat-consulta-bg);
}

.category-badge--queja {
  color: var(--ds-cat-queja);
  background: var(--ds-cat-queja-bg);
}

.category-badge--cancelacion {
  color: var(--ds-cat-cancelacion);
  background: var(--ds-cat-cancelacion-bg);
}
</style>
