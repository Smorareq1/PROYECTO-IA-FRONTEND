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
    <p class="examples__label">Ejemplos por categoría</p>
    <div class="examples__chips">
      <button
        v-for="(text, cat) in examples"
        :key="cat"
        class="examples__chip"
        :class="`examples__chip--${cat}`"
        @click="emit('select', text)"
      >
        {{ CATEGORY_LABELS[cat as Category] }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.examples__label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 10px;
}

.examples__chips { display: flex; flex-wrap: wrap; gap: 8px; }

.examples__chip {
  display: inline-flex;
  height: 30px;
  padding: 0 12px;
  border-radius: var(--ds-radius-full);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.15s;
}

.examples__chip--soporte_tecnico  { color: var(--ds-cat-soporte);      background: var(--ds-cat-soporte-bg);      border-color: var(--ds-cat-soporte); }
.examples__chip--facturacion      { color: var(--ds-cat-facturacion);   background: var(--ds-cat-facturacion-bg);  border-color: var(--ds-cat-facturacion); }
.examples__chip--consulta_general { color: var(--ds-cat-consulta);      background: var(--ds-cat-consulta-bg);     border-color: var(--ds-cat-consulta); }
.examples__chip--queja            { color: var(--ds-cat-queja);         background: var(--ds-cat-queja-bg);        border-color: var(--ds-cat-queja); }
.examples__chip--cancelacion      { color: var(--ds-cat-cancelacion);   background: var(--ds-cat-cancelacion-bg);  border-color: var(--ds-cat-cancelacion); }

.examples__chip:hover { filter: brightness(0.92); }
</style>
