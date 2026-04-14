<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronDown, LogOut, User } from 'lucide-vue-next'
import { useAuthStore } from '@/core/stores/auth.store'
import { ROLE_LABELS } from '@/core/config/constants'
import { storeToRefs } from 'pinia'

const store = useAuthStore()
const { user } = storeToRefs(store)
const router = useRouter()
const open = ref(false)

function initials(name: string) {
  return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

function logout() {
  open.value = false
  store.logout()
  router.push('/login')
}
</script>

<template>
  <div class="user-menu" v-if="user">
    <button class="user-menu__trigger" @click="open = !open">
      <div class="user-menu__avatar">{{ initials(user.full_name) }}</div>
      <div class="user-menu__info">
        <span class="user-menu__name">{{ user.full_name }}</span>
        <span class="user-menu__role">{{ ROLE_LABELS[user.role] }}</span>
      </div>
      <ChevronDown :size="14" class="user-menu__chevron" :class="{ 'user-menu__chevron--open': open }" />
    </button>

    <Transition name="dropdown">
      <div v-if="open" class="user-menu__dropdown">
        <div class="user-menu__dropdown-header">
          <p class="user-menu__dropdown-name">{{ user.full_name }}</p>
          <p class="user-menu__dropdown-email">{{ user.email }}</p>
        </div>
        <button class="user-menu__dropdown-item" @click="logout">
          <LogOut :size="14" />
          Cerrar sesión
        </button>
      </div>
    </Transition>

    <!-- Click outside -->
    <div v-if="open" class="user-menu__backdrop" @click="open = false" />
  </div>
</template>

<style scoped>
.user-menu { position: relative; }

.user-menu__trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-md);
  background: none;
  cursor: pointer;
  transition: background 0.15s;
}

.user-menu__trigger:hover { background: var(--ds-neutral-100); }
:global(.dark .user-menu__trigger:hover) { background: #27272A; }

.user-menu__avatar {
  width: 28px;
  height: 28px;
  border-radius: var(--ds-radius-sm);
  background: var(--ds-primary-500);
  color: #fff;
  font-size: var(--ds-text-xs);
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-menu__info {
  display: flex;
  flex-direction: column;
  text-align: left;
  line-height: 1.2;
}

.user-menu__name {
  font-size: var(--ds-text-sm);
  font-weight: 500;
  color: var(--ds-text-primary);
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-menu__role {
  font-size: 0.625rem;
  color: var(--ds-text-muted);
  text-transform: capitalize;
}

.user-menu__chevron {
  color: var(--ds-text-muted);
  transition: transform 0.2s;
}

.user-menu__chevron--open { transform: rotate(180deg); }

.user-menu__backdrop {
  position: fixed;
  inset: 0;
  z-index: 49;
}

.user-menu__dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  box-shadow: var(--ds-shadow-lg);
  z-index: 50;
  overflow: hidden;
}

:global(.dark .user-menu__dropdown) {
  background: #18181B;
  border-color: #3F3F46;
}

.user-menu__dropdown-header {
  padding: 12px 14px;
  border-bottom: 1px solid var(--ds-border);
}

.user-menu__dropdown-name {
  font-size: var(--ds-text-sm);
  font-weight: 600;
  color: var(--ds-text-primary);
}

.user-menu__dropdown-email {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  margin-top: 2px;
}

.user-menu__dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 10px 14px;
  background: none;
  border: none;
  color: var(--ds-text-secondary);
  font-size: var(--ds-text-sm);
  font-family: var(--ds-font-sans);
  cursor: pointer;
  text-align: left;
  transition: background 0.1s;
}

.user-menu__dropdown-item:hover {
  background: var(--ds-neutral-100);
  color: var(--ds-danger);
}

:global(.dark .user-menu__dropdown-item:hover) { background: #27272A; }

/* Transition */
.dropdown-enter-active, .dropdown-leave-active { transition: all 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
