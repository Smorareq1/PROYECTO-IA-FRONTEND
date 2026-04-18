import type { RouteRecordRaw } from 'vue-router'
import { landingRoutes } from '@/features/landing/routes'
import { ticketRoutes } from '@/features/tickets/routes'
import { classifierRoutes } from '@/features/classifier/routes'
import { metricsRoutes } from '@/features/metrics/routes'

export const routes: RouteRecordRaw[] = [
  ...landingRoutes,

  {
    path: '/app',
    component: () => import('@/design-system/layouts/AppShell.vue'),
    children: [
      {
        path: '',
        redirect: '/app/dashboard',
      },
      ...ticketRoutes,
      ...classifierRoutes,
      ...metricsRoutes,
      {
        path: '403',
        name: 'unauthorized',
        component: () => import('@/features/auth/pages/UnauthorizedPage.vue'),
      },
      {
        path: '404',
        name: 'not-found',
        component: () => import('@/features/auth/pages/UnauthorizedPage.vue'),
      },
    ],
  },

  { path: '/:pathMatch(.*)*', redirect: '/' },
]
