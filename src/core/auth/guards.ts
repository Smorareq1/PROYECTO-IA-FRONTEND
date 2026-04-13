import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { hasTokens } from './token-storage'
import type { Role } from '@/core/config/constants'

/**
 * Guard: require authentication
 */
export function requireAuth(
  _to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  next: NavigationGuardNext,
) {
  if (!hasTokens()) {
    next({ path: '/login', query: { redirect: _to.fullPath } })
  } else {
    next()
  }
}

/**
 * Guard factory: require specific role(s)
 */
export function requireRole(...roles: Role[]) {
  return (
    _to: RouteLocationNormalized,
    _from: RouteLocationNormalized,
    next: NavigationGuardNext,
  ) => {
    if (!hasTokens()) {
      next({ path: '/login', query: { redirect: _to.fullPath } })
      return
    }

    // Role check is done in the global beforeEach via the auth store
    // This is a placeholder — the actual check happens in middleware.ts
    const storedUser = localStorage.getItem('ticket_ai_user')
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser) as { role: Role }
        if (roles.includes(user.role)) {
          next()
          return
        }
      } catch {
        // Invalid stored user
      }
    }

    next({ path: '/app/403' })
  }
}
