import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'

/**
 * Vue Router instance
 */
export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})
