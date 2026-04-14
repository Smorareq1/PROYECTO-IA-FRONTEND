<script setup lang="ts">
interface Props {
  title?: string
  description?: string
}

defineProps<Props>()
</script>

<template>
  <div class="page-header">
    <div class="page-header__content">
      <h1 v-if="title" class="page-header__title">{{ title }}</h1>
      <p v-if="description" class="page-header__description">{{ description }}</p>
    </div>
    <div class="page-header__actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ds-border);
}

.page-header__title {
  font-size: var(--ds-text-2xl);
  font-weight: 700;
  color: var(--ds-text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.page-header__description {
  font-size: var(--ds-text-base);
  color: var(--ds-text-secondary);
  margin-top: 4px;
  max-width: 600px;
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

@media (max-width: 640px) {
  .page-header {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
