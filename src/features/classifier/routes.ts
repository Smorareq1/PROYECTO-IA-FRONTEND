import type { RouteRecordRaw } from 'vue-router'
import { requireAuth, requireRole } from '@/core/auth/guards'

export const classifierRoutes: RouteRecordRaw[] = [
  {
    path: 'playground',
    name: 'playground',
    component: () => import('./pages/PlaygroundPage.vue'),
    beforeEnter: [requireAuth, requireRole('agente', 'admin')],
    meta: { title: 'Playground' },
  },
]
