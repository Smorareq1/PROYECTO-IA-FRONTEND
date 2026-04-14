<script setup lang="ts">
import PageHeader from '@/design-system/molecules/PageHeader.vue'
import MetricsOverview from '../widgets/MetricsOverview.vue'
import ConfusionMatrix from '../widgets/ConfusionMatrix.vue'
import PerClassMetricsTable from '../widgets/PerClassMetricsTable.vue'
import KFoldResultsChart from '../widgets/KFoldResultsChart.vue'
import CategoryDistribution from '../widgets/CategoryDistribution.vue'
import { useModelMetrics } from '../composables/useModelMetrics'

const { metrics, confusionMatrix, kfolds, modelInfo, isLoading, error } = useModelMetrics()
</script>

<template>
  <div>
    <PageHeader
      title="Dashboard del Modelo"
      description="Métricas de rendimiento del clasificador Naïve Bayes en tiempo real."
    />

    <div v-if="isLoading" class="dashboard-skeleton">
      <div class="skeleton" style="height: 120px;" />
      <div class="dashboard-row">
        <div class="skeleton" style="height: 360px; flex: 2;" />
        <div class="skeleton" style="height: 360px; flex: 1;" />
      </div>
    </div>

    <div v-else-if="error" class="dashboard-error">
      <p>{{ error }}</p>
    </div>

    <template v-else-if="metrics">
      <div class="dashboard-sections">
        <!-- KPI cards -->
        <MetricsOverview :metrics="metrics" :model-info="modelInfo" />

        <!-- Confusion matrix + distribution -->
        <div class="dashboard-row">
          <div class="dashboard-col-main">
            <p class="section-label">Matriz de Confusión</p>
            <ConfusionMatrix v-if="confusionMatrix" :data="confusionMatrix" />
          </div>
          <div class="dashboard-col-side">
            <p class="section-label">Distribución del Dataset</p>
            <CategoryDistribution :metrics="metrics.per_class" />
          </div>
        </div>

        <!-- Per-class table -->
        <div>
          <p class="section-label">Métricas por Clase</p>
          <PerClassMetricsTable :metrics="metrics.per_class" />
        </div>

        <!-- K-Fold -->
        <div v-if="kfolds">
          <p class="section-label">Resultados K-Fold Cross-Validation</p>
          <KFoldResultsChart :data="kfolds" />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.dashboard-sections { display: flex; flex-direction: column; gap: 28px; }

.dashboard-skeleton { display: flex; flex-direction: column; gap: 16px; }

.dashboard-error {
  padding: 32px;
  text-align: center;
  color: var(--ds-danger);
  font-size: var(--ds-text-sm);
}

.dashboard-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: start;
}

@media (max-width: 900px) {
  .dashboard-row { grid-template-columns: 1fr; }
}

.section-label {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-secondary);
  margin-bottom: 10px;
}
</style>
