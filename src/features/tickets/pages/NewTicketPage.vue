<script setup lang="ts">
import { ref } from 'vue'
import { Send, CheckCircle, RotateCcw, ArrowRight } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { createTicketSchema } from '../models/ticket.schema'
import { useTicketMutations } from '../composables/useTicketMutations'
import type { Ticket } from '../models/ticket'
import CategoryBadge from '@/design-system/atoms/CategoryBadge.vue'
import ConfidenceBar from '@/design-system/molecules/ConfidenceBar.vue'
import PageHeader from '@/design-system/molecules/PageHeader.vue'

const router = useRouter()
const { create, isSubmitting } = useTicketMutations()

const { handleSubmit, defineField, errors, resetForm } = useForm({
  validationSchema: toTypedSchema(createTicketSchema),
})

const [subject, subjectAttrs] = defineField('subject')
const [description, descriptionAttrs] = defineField('description')

const result = ref<Ticket | null>(null)

const onSubmit = handleSubmit(async (values) => {
  const ticket = await create(values)
  if (ticket) result.value = ticket
})

function createAnother() {
  result.value = null
  resetForm()
}
</script>

<template>
  <div class="new-ticket-page">
    <PageHeader title="Nuevo Ticket" description="Describe tu solicitud y el sistema la clasificará automáticamente." />

    <!-- Form -->
    <div v-if="!result" class="new-ticket-form-wrap">
      <form class="new-ticket-form" @submit="onSubmit" novalidate>
        <div class="form-group">
          <label class="form-label" for="subject">Asunto *</label>
          <input
            id="subject"
            v-model="subject"
            v-bind="subjectAttrs"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.subject }"
            placeholder="Resumen breve del problema"
            maxlength="200"
          />
          <p v-if="errors.subject" class="form-error">{{ errors.subject }}</p>
        </div>

        <div class="form-group">
          <label class="form-label" for="description">Descripción *</label>
          <textarea
            id="description"
            v-model="description"
            v-bind="descriptionAttrs"
            class="form-textarea"
            :class="{ 'form-input--error': errors.description }"
            placeholder="Describe el problema con el mayor detalle posible…"
            rows="7"
            maxlength="2000"
          />
          <div class="form-footer-row">
            <p v-if="errors.description" class="form-error">{{ errors.description }}</p>
            <span class="form-char-count">{{ (description ?? '').length }} / 2000</span>
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          <svg v-if="isSubmitting" class="spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
          <Send v-else :size="16" />
          {{ isSubmitting ? 'Clasificando…' : 'Enviar y clasificar' }}
        </button>
      </form>
    </div>

    <!-- Result -->
    <div v-else class="new-ticket-result">
      <div class="result-card">
        <div class="result-card__check">
          <CheckCircle :size="40" />
        </div>
        <p class="result-card__id">{{ result.id }}</p>
        <h2 class="result-card__heading">Ticket clasificado correctamente</h2>

        <div class="result-card__category">
          <p class="result-card__category-label">Categoría asignada</p>
          <CategoryBadge :category="result.predicted_category" size="lg" />
        </div>

        <div class="result-card__bars">
          <p class="result-card__bars-label">Confianza por categoría</p>
          <ConfidenceBar
            :confidences="result.confidences"
            :highlight-category="result.predicted_category"
          />
        </div>

        <p class="result-card__message">
          Tu solicitud fue enrutada al departamento de
          <strong>{{ result.predicted_category.replace(/_/g, ' ') }}</strong>.
          Un agente se pondrá en contacto contigo pronto.
        </p>

        <div class="result-card__actions">
          <button class="result-btn result-btn--ghost" @click="createAnother">
            <RotateCcw :size="15" />
            Crear otro
          </button>
          <button class="result-btn result-btn--primary" @click="router.push('/app/mis-tickets')">
            Ver mis tickets
            <ArrowRight :size="15" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.new-ticket-page { max-width: 680px; }

/* Form */
.new-ticket-form-wrap {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  padding: 28px;
}

:global(.dark .new-ticket-form-wrap) { background: #18181B; border-color: #27272A; }

.new-ticket-form { display: flex; flex-direction: column; gap: 20px; }

.form-group { display: flex; flex-direction: column; gap: 6px; }

.form-label {
  font-size: var(--ds-text-sm);
  font-weight: 500;
  color: var(--ds-text-primary);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  font-size: var(--ds-text-base);
  font-family: var(--ds-font-sans);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-textarea { resize: vertical; min-height: 140px; }

.form-input:focus, .form-textarea:focus {
  border-color: var(--ds-primary-500);
  box-shadow: 0 0 0 3px rgba(15, 98, 254, 0.1);
}

.form-input--error { border-color: var(--ds-danger) !important; }

.form-error { font-size: var(--ds-text-xs); color: var(--ds-danger); }

.form-footer-row { display: flex; justify-content: space-between; }

.form-char-count { font-size: var(--ds-text-xs); color: var(--ds-text-muted); margin-left: auto; }

.submit-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  padding: 0 24px;
  background: var(--ds-primary-500);
  color: #fff;
  border: none;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-base);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: background 0.2s;
  align-self: flex-start;
}

.submit-btn:hover:not(:disabled) { background: var(--ds-primary-700); }
.submit-btn:disabled { opacity: 0.65; cursor: not-allowed; }

.spin { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Result */
.new-ticket-result { display: flex; justify-content: center; }

.result-card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-xl);
  padding: 36px 32px;
  max-width: 520px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeUp 0.3s ease-out;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

:global(.dark .result-card) { background: #18181B; border-color: #27272A; }

.result-card__check { color: var(--ds-success); }

.result-card__id {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.result-card__heading {
  font-size: var(--ds-text-xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.02em;
}

.result-card__category-label,
.result-card__bars-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--ds-text-muted);
  margin-bottom: 8px;
}

.result-card__message {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-secondary);
  line-height: 1.6;
  padding-top: 4px;
  border-top: 1px solid var(--ds-border);
}

.result-card__actions {
  display: flex;
  gap: 10px;
}

.result-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 38px;
  padding: 0 16px;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 500;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: all 0.15s;
}

.result-btn--ghost { border: 1px solid var(--ds-border); background: none; color: var(--ds-text-secondary); }
.result-btn--ghost:hover { background: var(--ds-neutral-100); }
.result-btn--primary { border: none; background: var(--ds-primary-500); color: #fff; }
.result-btn--primary:hover { background: var(--ds-primary-700); }
</style>
