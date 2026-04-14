<script setup lang="ts">
import TopBar from '@/design-system/molecules/TopBar.vue'
import PageDecorBackground from '@/design-system/atoms/PageDecorBackground.vue'
</script>

<template>
  <div class="app-shell">
    <TopBar />
    <PageDecorBackground />
    <main class="app-shell__main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--ds-surface);
}

.app-shell__main {
  position: relative;
  z-index: 1;
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
