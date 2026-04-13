import type { RouteRecordRaw } from 'vue-router'

// Import routes from each feature
import { landingRoutes } from '@/features/landing/routes'
import { authRoutes } from '@/features/auth/routes'

/**
 * All application routes composed from feature modules
 */
export const routes: RouteRecordRaw[] = [
  ...landingRoutes,
  ...authRoutes,

  // App routes (protected)
  {
    path: '/app',
    component: () => import('@/design-system/layouts/AppShell.vue'),
    children: [
      {
        path: '',
        redirect: '/app/playground',
      },
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

  // Catch-all
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]
