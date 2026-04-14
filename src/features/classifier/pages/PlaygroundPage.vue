<script setup lang="ts">
import { ref } from 'vue'
import PageHeader from '@/design-system/molecules/PageHeader.vue'
import ClassifyBox from '../widgets/ClassifyBox.vue'
import PredictionCard from '../widgets/PredictionCard.vue'
import PreprocessingTrace from '../widgets/PreprocessingTrace.vue'
import ExamplePrompts from '../widgets/ExamplePrompts.vue'
import { usePredict } from '../composables/usePredict'

const { classify, isLoading, result } = usePredict()
const inputText = ref('')

function onExample(text: string) {
  inputText.value = text
}

async function onClassify(text: string) {
  await classify(text)
}
</script>

<template>
  <div class="playground">
    <PageHeader
      title="Playground"
      description="Prueba el clasificador Naïve Bayes en tiempo real. Escribe cualquier texto de soporte."
    />

    <div class="playground__layout">
      <div class="playground__left">
        <ExamplePrompts @select="onExample" />
        <div style="margin-top: 16px;">
          <ClassifyBox v-model="inputText" :is-loading="isLoading" @classify="onClassify" />
        </div>
      </div>

      <div class="playground__right">
        <div v-if="!result && !isLoading" class="playground__empty">
          <p class="playground__empty-text">El resultado aparecerá aquí tras clasificar un texto.</p>
        </div>

        <div v-if="isLoading" class="playground__skeleton">
          <div class="skeleton" style="height: 100px; margin-bottom: 12px;" />
          <div class="skeleton" style="height: 200px;" />
        </div>

        <template v-if="result">
          <PredictionCard :prediction="result" />
          <div style="margin-top: 12px;">
            <PreprocessingTrace :prediction="result" />
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.playground__layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: start;
}

@media (max-width: 900px) {
  .playground__layout { grid-template-columns: 1fr; }
}

.playground__empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  background: var(--ds-surface);
  border: 1px dashed var(--ds-border);
  border-radius: var(--ds-radius-lg);
}

:global(.dark .playground__empty) { background: #18181B; }

.playground__empty-text {
  font-size: var(--ds-text-sm);
  color: var(--ds-text-muted);
  text-align: center;
  max-width: 220px;
}

.playground__skeleton { display: flex; flex-direction: column; }
</style>
