<script setup lang="ts">
import PageHeader from '@/design-system/molecules/PageHeader.vue'
import ModelInfoCard from '../widgets/ModelInfoCard.vue'
import KFoldVarianceCard from '../widgets/KFoldVarianceCard.vue'
import VocabularyCard from '../widgets/VocabularyCard.vue'
import { useModelMetrics } from '../composables/useModelMetrics'

const { modelInfo, kfolds, isLoading, error } = useModelMetrics()
</script>

<template>
  <div>
    <PageHeader
      title="Salud del Modelo"
      description="Información técnica del clasificador, varianza K-Fold y vocabulario aprendido."
    />

    <div v-if="isLoading" class="skeleton-grid">
      <div class="skeleton" style="height: 220px;" />
      <div class="skeleton" style="height: 220px;" />
      <div class="skeleton" style="height: 300px; grid-column: 1 / -1;" />
    </div>

    <div v-else-if="error" class="error-msg">{{ error }}</div>

    <template v-else>
      <div class="health-grid">
        <ModelInfoCard v-if="modelInfo" :info="modelInfo" />
        <KFoldVarianceCard v-if="kfolds" :data="kfolds" />
      </div>

      <div style="margin-top: 24px;">
        <VocabularyCard />
      </div>
    </template>
  </div>
</template>

<style scoped>
.health-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .health-grid { grid-template-columns: 1fr; }
}

.skeleton-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.error-msg { color: var(--ds-danger); font-size: var(--ds-text-sm); padding: 16px; }
</style>
