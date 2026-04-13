<script setup lang="ts">
import AppLogo from '@/design-system/components/AppLogo.vue'
import ThemeToggle from './ThemeToggle.vue'
import { LogIn } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <header class="topbar">
    <div class="topbar__inner">
      <div class="topbar__left">
        <AppLogo />
      </div>

      <nav class="topbar__nav">
        <!-- Navigation items will be dynamic based on role -->
        <!-- For now, placeholder links -->
      </nav>

      <div class="topbar__right">
        <ThemeToggle />
        <router-link to="/login" class="topbar__login-btn">
          <LogIn :size="16" />
          <span>Iniciar sesión</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--ds-surface);
  border-bottom: 1px solid var(--ds-border);
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.85);
}

:global(.dark .topbar) {
  background: rgba(9, 9, 11, 0.9);
  border-bottom-color: #27272A;
}

.topbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 32px;
  height: 56px;
}

.topbar__left {
  display: flex;
  align-items: center;
}

.topbar__nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.topbar__right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.topbar__login-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: var(--ds-radius-md);
  background: var(--ds-primary-500);
  color: #fff;
  font-size: var(--ds-text-sm);
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.topbar__login-btn:hover {
  background: var(--ds-primary-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 98, 254, 0.3);
}

.topbar__login-btn:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .topbar__inner {
    padding: 0 16px;
  }

  .topbar__login-btn span {
    display: none;
  }
}
</style>
