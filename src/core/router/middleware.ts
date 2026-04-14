import { router } from './index'
import { hasTokens } from '@/core/auth/token-storage'

/**
 * Global navigation middleware:
 * - Redirect authenticated users away from /login
 * - All per-route auth checks are handled by beforeEnter guards in each feature's routes.ts
 */
router.beforeEach((to, _from, next) => {
  const isPublic = to.meta.public === true

  // Redirect logged-in users away from /login
  if (isPublic && hasTokens() && to.path === '/login') {
    next('/app')
    return
  }

  next()
})

export { router as routerWithMiddleware }
