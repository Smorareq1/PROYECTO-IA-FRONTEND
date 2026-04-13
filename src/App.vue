<script setup lang="ts">
import ToastContainer from '@/design-system/components/ToastContainer.vue'
</script>

<template>
  <router-view />
  <ToastContainer />
</template>

<style>
/* App-level transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.2s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
}
</style>
