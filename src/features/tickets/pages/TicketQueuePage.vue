<script setup lang="ts">
import { ref } from 'vue'
import PageHeader from '@/design-system/molecules/PageHeader.vue'
import TicketTable from '../widgets/TicketTable.vue'
import TicketFilters from '../widgets/TicketFilters.vue'
import TicketDetailPanel from '../widgets/TicketDetailPanel.vue'
import type { Ticket } from '../models/ticket'
import { useTicketList } from '../composables/useTicketList'

const { tickets, isLoading } = useTicketList()
const panelTicket = ref<Ticket | null>(null)
</script>

<template>
  <div>
    <PageHeader
      title="Cola de Tickets"
      description="Gestiona y clasifica las solicitudes entrantes."
    />
    <TicketFilters />
    <TicketTable :tickets="tickets" :is-loading="isLoading" @select="t => panelTicket = t" />

    <TicketDetailPanel
      v-if="panelTicket"
      :ticket="panelTicket"
      @close="panelTicket = null"
    />
  </div>
</template>
