<script setup lang="ts">
import TopBar from '@/design-system/molecules/TopBar.vue'
</script>

<template>
  <div class="app-shell">
    <TopBar />
    <main class="app-shell__main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--ds-surface);
}

.app-shell__main {
  flex: 1;
  padding: 24px 32px;
  max-width: 1320px;
  width: 100%;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .app-shell__main {
    padding: 16px;
  }
}
</style>
