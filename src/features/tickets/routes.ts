import type { RouteRecordRaw } from 'vue-router'
import { requireAuth, requireRole } from '@/core/auth/guards'

export const ticketRoutes: RouteRecordRaw[] = [
  {
    path: 'nuevo-ticket',
    name: 'new-ticket',
    component: () => import('./pages/NewTicketPage.vue'),
    beforeEnter: [requireAuth, requireRole('cliente', 'agente', 'admin')],
    meta: { title: 'Nuevo Ticket' },
  },
  {
    path: 'mis-tickets',
    name: 'my-tickets',
    component: () => import('./pages/MyTicketsPage.vue'),
    beforeEnter: [requireAuth],
    meta: { title: 'Mis Tickets' },
  },
  {
    path: 'cola',
    name: 'ticket-queue',
    component: () => import('./pages/TicketQueuePage.vue'),
    beforeEnter: [requireAuth, requireRole('agente', 'admin')],
    meta: { title: 'Cola de Tickets' },
  },
  {
    path: 'tickets/:id',
    name: 'ticket-detail',
    component: () => import('./pages/TicketDetailPage.vue'),
    beforeEnter: [requireAuth],
    meta: { title: 'Detalle de Ticket' },
  },
]
