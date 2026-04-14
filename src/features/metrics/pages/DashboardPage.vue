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
        <section>
          <header class="section-head">
            <span class="section-head__num">01</span>
            <div>
              <h2 class="section-head__title">Métricas clave</h2>
              <p class="section-head__hint">Rendimiento global del modelo.</p>
            </div>
          </header>
          <MetricsOverview :metrics="metrics" :model-info="modelInfo" />
        </section>

        <!-- Confusion matrix + distribution -->
        <section>
          <header class="section-head">
            <span class="section-head__num">02</span>
            <div>
              <h2 class="section-head__title">Matriz de Confusión y Distribución</h2>
              <p class="section-head__hint">Errores de clasificación y balance del dataset.</p>
            </div>
          </header>
          <div class="dashboard-row">
            <div class="dashboard-col-main">
              <ConfusionMatrix v-if="confusionMatrix" :data="confusionMatrix" />
            </div>
            <div class="dashboard-col-side">
              <CategoryDistribution :metrics="metrics.per_class" />
            </div>
          </div>
        </section>

        <!-- Per-class table -->
        <section>
          <header class="section-head">
            <span class="section-head__num">03</span>
            <div>
              <h2 class="section-head__title">Métricas por Clase</h2>
              <p class="section-head__hint">Precision, Recall y F1 para cada categoría.</p>
            </div>
          </header>
          <PerClassMetricsTable :metrics="metrics.per_class" />
        </section>

        <!-- K-Fold -->
        <section v-if="kfolds">
          <header class="section-head">
            <span class="section-head__num">04</span>
            <div>
              <h2 class="section-head__title">K-Fold Cross-Validation</h2>
              <p class="section-head__hint">Estabilidad del modelo a través de los folds.</p>
            </div>
          </header>
          <KFoldResultsChart :data="kfolds" />
        </section>
      </div>
    </template>
  </div>
</template>

<style scoped>
.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

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

@media (max-width: 960px) {
  .dashboard-row { grid-template-columns: 1fr; }
}

/* ── Section header (editorial, numbered) ───────────── */
.section-head {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 16px;
}

.section-head__num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
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

.section-head__title {
  font-size: var(--ds-text-base);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.01em;
  margin: 0 0 2px;
  line-height: 1.2;
}

.section-head__hint {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin: 0;
  line-height: 1.4;
}
</style>
