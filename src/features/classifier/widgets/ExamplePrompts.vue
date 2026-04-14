<script setup lang="ts">
import type { Category } from '@/core/config/constants'
import { CATEGORY_LABELS } from '@/core/config/constants'

const emit = defineEmits<{ select: [text: string] }>()

const examples: Record<Category, string> = {
  soporte_tecnico:  'No puedo acceder a mi cuenta, el sistema me da un error 403 al intentar iniciar sesión.',
  facturacion:      'Me cobraron dos veces la misma suscripción este mes y quiero que me hagan el reembolso.',
  consulta_general: '¿Cuáles son los horarios de atención al cliente y qué canales tienen disponibles?',
  queja:            'El servicio ha sido muy deficiente, llevo tres días sin respuesta y nadie me ha ayudado.',
  cancelacion:      'Deseo cancelar mi plan premium y darme de baja definitivamente del servicio.',
}
</script>

<template>
  <div class="examples">
    <div class="examples__chips">
      <button
        v-for="(text, cat) in examples"
        :key="cat"
        class="examples__chip"
        :class="`examples__chip--${cat}`"
        @click="emit('select', text)"
        :title="text"
      >
        <span class="examples__chip-dot"></span>
        <span class="examples__chip-label">{{ CATEGORY_LABELS[cat as Category] }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.examples__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.examples__chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 0 14px;
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  border: 1px solid var(--ds-border);
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

:global(.dark .examples__chip) {
  background: #18181B;
  border-color: #27272A;
}

.examples__chip-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.examples__chip-label { letter-spacing: 0.01em; }

.examples__chip--soporte_tecnico  .examples__chip-dot { background: var(--ds-cat-soporte); }
.examples__chip--facturacion      .examples__chip-dot { background: var(--ds-cat-facturacion); }
.examples__chip--consulta_general .examples__chip-dot { background: var(--ds-cat-consulta); }
.examples__chip--queja            .examples__chip-dot { background: var(--ds-cat-queja); }
.examples__chip--cancelacion      .examples__chip-dot { background: var(--ds-cat-cancelacion); }

.examples__chip--soporte_tecnico:hover  { border-color: var(--ds-cat-soporte);      box-shadow: 0 2px 0 var(--ds-cat-soporte);      transform: translateY(-1px); }
.examples__chip--facturacion:hover      { border-color: var(--ds-cat-facturacion);   box-shadow: 0 2px 0 var(--ds-cat-facturacion);   transform: translateY(-1px); }
.examples__chip--consulta_general:hover { border-color: var(--ds-cat-consulta);      box-shadow: 0 2px 0 var(--ds-cat-consulta);      transform: translateY(-1px); }
.examples__chip--queja:hover            { border-color: var(--ds-cat-queja);         box-shadow: 0 2px 0 var(--ds-cat-queja);         transform: translateY(-1px); }
.examples__chip--cancelacion:hover      { border-color: var(--ds-cat-cancelacion);   box-shadow: 0 2px 0 var(--ds-cat-cancelacion);   transform: translateY(-1px); }

.examples__chip:active { transform: translateY(0); box-shadow: none; }
</style>
