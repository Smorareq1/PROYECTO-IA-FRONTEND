<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue'
import { PenLine, Zap, BarChart3, Sparkles, ArrowDown } from 'lucide-vue-next'
import PageHeader from '@/design-system/molecules/PageHeader.vue'
import ClassifyBox from '../widgets/ClassifyBox.vue'
import PredictionCard from '../widgets/PredictionCard.vue'
import ExamplePrompts from '../widgets/ExamplePrompts.vue'
import { CATEGORY_LABELS } from '@/core/config/constants'
import { usePredict } from '../composables/usePredict'

const { classify, isLoading, result } = usePredict()
const inputText = ref('')
const activeTab = ref<'result' | 'tokens' | 'probs'>('result')
const resultRef = ref<HTMLElement>()

type TabKey = 'result' | 'tokens' | 'probs'
const tabs: { key: TabKey; label: string; icon: typeof Sparkles }[] = [
  { key: 'result', label: 'Predicción',       icon: Sparkles },
  { key: 'tokens', label: 'Tokens',           icon: PenLine  },
  { key: 'probs',  label: 'Probabilidades',   icon: BarChart3 },
]

const currentStep = computed(() => {
  if (isLoading.value) return 2
  if (result.value)    return 3
  if (inputText.value.trim()) return 2
  return 1
})

const logProbEntries = computed(() => {
  if (!result.value) return []
  return Object.entries(result.value.log_probs).sort(([, a], [, b]) => b - a)
})

function onExample(text: string) {
  inputText.value = text
}

async function onClassify(text: string) {
  await classify(text)
  activeTab.value = 'result'
  await nextTick()
  resultRef.value?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
}

watch(result, (r) => { if (r) activeTab.value = 'result' })
</script>

<template>
  <div class="playground">
    <PageHeader
      title="Playground"
      description="Prueba el clasificador Naïve Bayes en tiempo real. Escribe cualquier texto de soporte."
    />

    <!-- Stepper -->
    <ol class="pg-steps" aria-label="Flujo de clasificación">
      <li
        v-for="(label, i) in ['Escribe o elige un ejemplo', 'Clasifica', 'Analiza el resultado']"
        :key="i"
        class="pg-step"
        :class="{
          'pg-step--active':   currentStep === i + 1,
          'pg-step--complete': currentStep > i + 1,
        }"
      >
        <span class="pg-step__num">{{ String(i + 1).padStart(2, '0') }}</span>
        <span class="pg-step__label">{{ label }}</span>
        <span v-if="i < 2" class="pg-step__connector" aria-hidden="true"></span>
      </li>
    </ol>

    <div class="pg-layout">
      <!-- Left column -->
      <section class="pg-col">
        <div class="pg-card">
          <header class="pg-card__header">
            <span class="pg-card__num">01</span>
            <div>
              <h2 class="pg-card__title">Empieza con un ejemplo</h2>
              <p class="pg-card__hint">Selecciona una categoría o escribe tu propio texto.</p>
            </div>
          </header>
          <div class="pg-card__body">
            <ExamplePrompts @select="onExample" />
          </div>
        </div>

        <div class="pg-card">
          <header class="pg-card__header">
            <span class="pg-card__num">02</span>
            <div>
              <h2 class="pg-card__title">Tu texto</h2>
              <p class="pg-card__hint">Ctrl + Enter para clasificar al instante.</p>
            </div>
          </header>
          <div class="pg-card__body pg-card__body--flush">
            <ClassifyBox v-model="inputText" :is-loading="isLoading" @classify="onClassify" />
          </div>
        </div>
      </section>

      <!-- Right column: result -->
      <section class="pg-col" ref="resultRef">
        <div class="pg-card pg-result">
          <header class="pg-card__header">
            <span class="pg-card__num">03</span>
            <div>
              <h2 class="pg-card__title">Resultado</h2>
              <p class="pg-card__hint">Explora la predicción, los tokens y las probabilidades.</p>
            </div>
          </header>

          <!-- Tabs -->
          <nav class="pg-tabs" role="tablist" :class="{ 'pg-tabs--disabled': !result }">
            <button
              v-for="t in tabs"
              :key="t.key"
              role="tab"
              class="pg-tab"
              :class="{ 'pg-tab--active': activeTab === t.key }"
              :aria-selected="activeTab === t.key"
              :disabled="!result"
              @click="activeTab = t.key"
            >
              <component :is="t.icon" :size="14" />
              <span>{{ t.label }}</span>
            </button>
            <div class="pg-tabs__indicator" :data-tab="activeTab" aria-hidden="true"></div>
          </nav>

          <div class="pg-card__body">
            <!-- Empty state -->
            <div v-if="!result && !isLoading" class="pg-empty">
              <div class="pg-empty__art" aria-hidden="true">
                <span class="pg-empty__shape pg-empty__shape--circle"></span>
                <span class="pg-empty__shape pg-empty__shape--square"></span>
                <span class="pg-empty__shape pg-empty__shape--block"></span>
                <span class="pg-empty__shape pg-empty__shape--line"></span>
              </div>
              <p class="pg-empty__title">Aún no hay predicción</p>
              <p class="pg-empty__text">
                Elige un ejemplo o escribe un texto y pulsa <kbd>Clasificar</kbd>.
                El resultado se mostrará aquí.
              </p>
              <ArrowDown :size="16" class="pg-empty__arrow" />
            </div>

            <!-- Loading state -->
            <div v-else-if="isLoading" class="pg-loading">
              <div class="pg-loading__bar"></div>
              <p class="pg-loading__label">Analizando texto…</p>
              <div class="pg-loading__dots">
                <span></span><span></span><span></span>
              </div>
            </div>

            <!-- Tab panels -->
            <transition name="pg-fade" mode="out-in">
              <!-- Predicción -->
              <div v-if="result && activeTab === 'result'" key="result" class="pg-panel">
                <PredictionCard :prediction="result" />
              </div>

              <!-- Tokens -->
              <div v-else-if="result && activeTab === 'tokens'" key="tokens" class="pg-panel">
                <div class="pg-panel__meta">
                  <span class="pg-panel__meta-label">Tokens extraídos</span>
                  <span class="pg-panel__meta-value">{{ result.tokens.length }}</span>
                </div>
                <div class="pg-tokens">
                  <span
                    v-for="(token, i) in result.tokens"
                    :key="i"
                    class="pg-token"
                    :style="{ animationDelay: `${i * 18}ms` }"
                  >
                    {{ token }}
                  </span>
                </div>
              </div>

              <!-- Probabilidades -->
              <div v-else-if="result && activeTab === 'probs'" key="probs" class="pg-panel">
                <div class="pg-panel__meta">
                  <span class="pg-panel__meta-label">Log-probabilidades por clase</span>
                  <span class="pg-panel__meta-value">{{ logProbEntries.length }}</span>
                </div>
                <ul class="pg-probs">
                  <li
                    v-for="([cat, lp], i) in logProbEntries"
                    :key="cat"
                    class="pg-prob"
                    :class="{ 'pg-prob--top': cat === result.category }"
                    :style="{ animationDelay: `${i * 40}ms` }"
                  >
                    <span class="pg-prob__rank">{{ String(i + 1).padStart(2, '0') }}</span>
                    <span class="pg-prob__cat">{{ CATEGORY_LABELS[cat as keyof typeof CATEGORY_LABELS] }}</span>
                    <span class="pg-prob__val">{{ lp.toFixed(4) }}</span>
                  </li>
                </ul>
              </div>
            </transition>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ── Stepper ─────────────────────────────────────────────── */
.pg-steps {
  list-style: none;
  display: flex;
  gap: 4px;
  margin: 0 0 24px;
  padding: 0;
  flex-wrap: wrap;
}

.pg-step {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px 10px 14px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-sm);
  background: var(--ds-surface);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  color: var(--ds-text-muted);
  transition: color 0.2s ease, border-color 0.2s ease, background 0.2s ease;
  flex: 1 1 auto;
  min-width: 180px;
}

:global(.dark .pg-step) { background: #18181B; border-color: #27272A; }

.pg-step__num {
  font-family: var(--ds-font-mono);
  font-size: 0.6875rem;
  padding: 2px 6px;
  border-radius: 3px;
  background: var(--ds-neutral-100);
  color: var(--ds-text-muted);
  letter-spacing: 0.02em;
  transition: background 0.2s ease, color 0.2s ease;
}

:global(.dark .pg-step__num) { background: #27272A; }

.pg-step__label {
  letter-spacing: 0.01em;
}

.pg-step__connector {
  position: absolute;
  right: -12px;
  top: 50%;
  width: 16px;
  height: 2px;
  background: var(--ds-border);
  transform: translateY(-50%);
  z-index: 1;
}

.pg-step--active {
  color: var(--ds-text-primary);
  border-color: var(--ds-primary-500);
  box-shadow: 0 2px 0 var(--ds-primary-500);
}

.pg-step--active .pg-step__num {
  background: var(--ds-primary-500);
  color: #fff;
}

.pg-step--complete {
  color: var(--ds-text-primary);
  border-color: var(--ds-text-primary);
}

.pg-step--complete .pg-step__num {
  background: var(--ds-text-primary);
  color: var(--ds-surface);
}

/* ── Layout ─────────────────────────────────────────────── */
.pg-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

@media (max-width: 960px) {
  .pg-layout { grid-template-columns: 1fr; }
}

.pg-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

/* ── Card ─────────────────────────────────────────────── */
.pg-card {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  overflow: hidden;
}

:global(.dark .pg-card) { background: #18181B; border-color: #27272A; }

.pg-card__header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px 20px 14px;
  border-bottom: 1px solid var(--ds-border);
}

:global(.dark .pg-card__header) { border-bottom-color: #27272A; }

.pg-card__num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 26px;
  padding: 0 8px;
  border-radius: 3px;
  background: var(--ds-text-primary);
  color: var(--ds-surface);
  font-family: var(--ds-font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.pg-card__title {
  font-size: var(--ds-text-base);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.01em;
  margin: 0 0 2px;
  line-height: 1.2;
}

.pg-card__hint {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin: 0;
  line-height: 1.4;
}

.pg-card__body {
  padding: 18px 20px;
}

.pg-card__body--flush { padding: 0; }

/* ── Tabs ─────────────────────────────────────────────── */
.pg-tabs {
  position: relative;
  display: flex;
  gap: 2px;
  padding: 0 20px;
  border-bottom: 1px solid var(--ds-border);
  background: var(--ds-surface-raised);
}

:global(.dark .pg-tabs) {
  background: #0F0F11;
  border-bottom-color: #27272A;
}

.pg-tabs--disabled { opacity: 0.55; }

.pg-tab {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 12px 14px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--ds-text-muted);
  font-size: var(--ds-text-sm);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: color 0.2s ease;
  margin-bottom: -1px;
}

.pg-tab:hover:not(:disabled) { color: var(--ds-text-primary); }
.pg-tab:disabled { cursor: not-allowed; }

.pg-tab--active {
  color: var(--ds-text-primary);
  border-bottom-color: var(--ds-primary-500);
}

/* ── Empty state ─────────────────────────────────────── */
.pg-empty {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 24px 32px;
  min-height: 260px;
  text-align: center;
  overflow: hidden;
}

.pg-empty__art {
  position: relative;
  width: 96px;
  height: 96px;
  margin-bottom: 4px;
}

.pg-empty__shape { position: absolute; }

.pg-empty__shape--circle {
  width: 64px; height: 64px;
  border: 1.5px solid var(--ds-primary-500);
  border-radius: 50%;
  top: 8px; left: 12px;
  opacity: 0.35;
  animation: pgFloat 4.2s ease-in-out infinite;
}

.pg-empty__shape--square {
  width: 36px; height: 36px;
  border: 1.5px solid var(--ds-neutral-300);
  top: 44px; right: 4px;
  transform: rotate(14deg);
  opacity: 0.6;
  animation: pgFloat 5s ease-in-out infinite reverse;
}

:global(.dark .pg-empty__shape--square) { border-color: var(--ds-neutral-200); }

.pg-empty__shape--block {
  width: 18px; height: 18px;
  background: var(--ds-primary-500);
  top: 6px; right: 18px;
  opacity: 0.9;
}

.pg-empty__shape--line {
  width: 44px; height: 3px;
  background: var(--ds-text-primary);
  bottom: 14px; left: 6px;
  opacity: 0.6;
}

@keyframes pgFloat {
  0%, 100% { transform: translateY(0) rotate(0); }
  50%      { transform: translateY(-6px) rotate(2deg); }
}

.pg-empty__shape--square { animation-name: pgFloatRot; }
@keyframes pgFloatRot {
  0%, 100% { transform: rotate(14deg) translateY(0); }
  50%      { transform: rotate(18deg) translateY(-5px); }
}

.pg-empty__title {
  font-size: var(--ds-text-sm);
  font-weight: 700;
  color: var(--ds-text-primary);
  margin: 0;
}

.pg-empty__text {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  max-width: 280px;
  margin: 0;
  line-height: 1.55;
}

.pg-empty__text kbd {
  font-family: var(--ds-font-mono);
  font-size: 0.6875rem;
  padding: 1px 5px;
  border: 1px solid var(--ds-border);
  border-bottom-width: 2px;
  border-radius: 3px;
  background: var(--ds-surface-raised);
  color: var(--ds-text-primary);
}

.pg-empty__arrow {
  color: var(--ds-text-muted);
  margin-top: 4px;
  animation: pgBounce 1.6s ease-in-out infinite;
}

@keyframes pgBounce {
  0%, 100% { transform: translateY(0); opacity: 0.4; }
  50%      { transform: translateY(4px); opacity: 1; }
}

/* ── Loading ─────────────────────────────────────────── */
.pg-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 48px 24px;
  min-height: 220px;
}

.pg-loading__bar {
  position: relative;
  width: 60%;
  max-width: 240px;
  height: 3px;
  background: var(--ds-neutral-100);
  border-radius: 2px;
  overflow: hidden;
}

:global(.dark .pg-loading__bar) { background: #27272A; }

.pg-loading__bar::after {
  content: '';
  position: absolute;
  top: 0; bottom: 0;
  width: 40%;
  background: var(--ds-primary-500);
  animation: pgSlide 1.2s ease-in-out infinite;
}

@keyframes pgSlide {
  0%   { left: -40%; }
  100% { left: 100%; }
}

.pg-loading__label {
  font-size: var(--ds-text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  color: var(--ds-text-muted);
  margin: 0;
}

.pg-loading__dots {
  display: flex;
  gap: 5px;
}

.pg-loading__dots span {
  width: 6px; height: 6px;
  background: var(--ds-text-muted);
  border-radius: 50%;
  animation: pgDot 1.1s ease-in-out infinite;
}

.pg-loading__dots span:nth-child(2) { animation-delay: 0.15s; }
.pg-loading__dots span:nth-child(3) { animation-delay: 0.3s; }

@keyframes pgDot {
  0%, 80%, 100% { opacity: 0.3; transform: scale(1); }
  40%           { opacity: 1;   transform: scale(1.3); }
}

/* ── Panels ──────────────────────────────────────────── */
.pg-panel { min-height: 200px; }

.pg-panel__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  margin-bottom: 14px;
  border-bottom: 1px solid var(--ds-border);
}

:global(.dark .pg-panel__meta) { border-bottom-color: #27272A; }

.pg-panel__meta-label {
  font-size: var(--ds-text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ds-text-muted);
}

.pg-panel__meta-value {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-sm);
  font-weight: 700;
  color: var(--ds-text-primary);
}

.pg-fade-enter-active,
.pg-fade-leave-active { transition: opacity 0.22s ease, transform 0.22s ease; }
.pg-fade-enter-from   { opacity: 0; transform: translateY(6px); }
.pg-fade-leave-to     { opacity: 0; transform: translateY(-4px); }

/* Tokens */
.pg-tokens {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.pg-token {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 3px;
  background: var(--ds-neutral-100);
  border: 1px solid var(--ds-border);
  color: var(--ds-text-primary);
  font-family: var(--ds-font-mono);
  font-size: 0.75rem;
  opacity: 0;
  animation: pgTokenIn 0.3s ease-out forwards;
}

:global(.dark .pg-token) {
  background: #27272A;
  border-color: #3F3F46;
}

@keyframes pgTokenIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Log-probs */
.pg-probs {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.pg-prob {
  display: grid;
  grid-template-columns: 40px 1fr auto;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid var(--ds-border);
  border-radius: 3px;
  background: var(--ds-surface);
  font-size: var(--ds-text-sm);
  opacity: 0;
  animation: pgProbIn 0.3s ease-out forwards;
  transition: border-color 0.15s ease;
}

:global(.dark .pg-prob) { background: #18181B; border-color: #27272A; }

.pg-prob__rank {
  font-family: var(--ds-font-mono);
  font-size: 0.6875rem;
  color: var(--ds-text-muted);
  letter-spacing: 0.02em;
}

.pg-prob__cat {
  color: var(--ds-text-primary);
  font-weight: 500;
}

.pg-prob__val {
  font-family: var(--ds-font-mono);
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  text-align: right;
}

.pg-prob--top {
  border-color: var(--ds-primary-500);
  box-shadow: 0 2px 0 var(--ds-primary-500);
}

.pg-prob--top .pg-prob__cat   { color: var(--ds-primary-700); font-weight: 700; }
.pg-prob--top .pg-prob__rank  { color: var(--ds-primary-500); }
.pg-prob--top .pg-prob__val   { color: var(--ds-primary-700); font-weight: 600; }

:global(.dark .pg-prob--top .pg-prob__cat),
:global(.dark .pg-prob--top .pg-prob__val) { color: #93C5FD; }

@keyframes pgProbIn {
  from { opacity: 0; transform: translateX(-6px); }
  to   { opacity: 1; transform: translateX(0); }
}

@media (prefers-reduced-motion: reduce) {
  .pg-empty__arrow,
  .pg-empty__shape--circle,
  .pg-empty__shape--square,
  .pg-loading__bar::after,
  .pg-loading__dots span,
  .pg-token,
  .pg-prob { animation: none; opacity: 1; }
}
</style>
