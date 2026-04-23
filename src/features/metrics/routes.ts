import type { RouteRecordRaw } from 'vue-router'
import { requireAuth, requireRole } from '@/core/auth/guards'

export const metricsRoutes: RouteRecordRaw[] = [
  {
    path: 'dashboard',
    name: 'dashboard',
    component: () => import('./pages/DashboardPage.vue'),
    beforeEnter: [requireAuth, requireRole('admin')],
    meta: { title: 'Dashboard' },
  },
]
