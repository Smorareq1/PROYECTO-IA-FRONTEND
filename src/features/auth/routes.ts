import type { RouteRecordRaw } from 'vue-router'

export const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/design-system/layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('./pages/LoginPage.vue'),
      },
    ],
    meta: { public: true },
  },
]
