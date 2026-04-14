<script setup lang="ts">
import { ref } from 'vue'
import { Plus } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import PageHeader from '@/design-system/molecules/PageHeader.vue'
import TicketTable from '../widgets/TicketTable.vue'
import TicketFilters from '../widgets/TicketFilters.vue'
import TicketDetailPanel from '../widgets/TicketDetailPanel.vue'
import type { Ticket } from '../models/ticket'
import { useTicketList } from '../composables/useTicketList'

const router = useRouter()
const { tickets, isLoading, select } = useTicketList()
const panelTicket = ref<Ticket | null>(null)

function onSelect(ticket: Ticket) {
  panelTicket.value = ticket
  select(ticket)
}
</script>

<template>
  <div>
    <PageHeader title="Mis Tickets" description="Historial de todas tus solicitudes enviadas.">
      <template #actions>
        <button class="new-btn" @click="router.push('/app/nuevo-ticket')">
          <Plus :size="16" />
          Nuevo ticket
        </button>
      </template>
    </PageHeader>

    <TicketFilters />
    <TicketTable :tickets="tickets" :is-loading="isLoading" @select="onSelect" />

    <TicketDetailPanel
      v-if="panelTicket"
      :ticket="panelTicket"
      @close="panelTicket = null"
    />
  </div>
</template>

<style scoped>
.new-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 36px;
  padding: 0 16px;
  background: var(--ds-primary-500);
  color: #fff;
  border: none;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 500;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: background 0.2s;
}

.new-btn:hover { background: var(--ds-primary-700); }
</style>
