import type { RouteRecordRaw } from 'vue-router'
import { landingRoutes } from '@/features/landing/routes'
import { authRoutes } from '@/features/auth/routes'
import { ticketRoutes } from '@/features/tickets/routes'
import { classifierRoutes } from '@/features/classifier/routes'
import { analyticsRoutes } from '@/features/analytics/routes'

export const routes: RouteRecordRaw[] = [
  ...landingRoutes,
  ...authRoutes,

  {
    path: '/app',
    component: () => import('@/design-system/layouts/AppShell.vue'),
    children: [
      {
        path: '',
        redirect: () => {
          try {
            const raw = localStorage.getItem('auth')
            const user = raw ? (JSON.parse(raw) as { user?: { role?: string } }).user : null
            if (user?.role === 'cliente') return '/app/mis-tickets'
            if (user?.role === 'agente') return '/app/cola'
            if (user?.role === 'admin') return '/app/dashboard'
          } catch { /* empty */ }
          return '/app/playground'
        },
      },
      ...ticketRoutes,
      ...classifierRoutes,
      ...analyticsRoutes,
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
