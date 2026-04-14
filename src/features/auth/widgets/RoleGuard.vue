<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/core/stores/auth.store'
import type { Role } from '@/core/config/constants'

const props = defineProps<{
  roles: Role[]
}>()

const { role } = storeToRefs(useAuthStore())
const allowed = computed(() => !!role.value && props.roles.includes(role.value))
</script>

<template>
  <slot v-if="allowed" />
</template>
