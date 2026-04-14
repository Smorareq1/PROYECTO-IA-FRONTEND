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

    // Pinia persist stores the auth store under key 'auth' as { user: { role, ... } }
    try {
      const raw = localStorage.getItem('auth')
      const stored = raw ? (JSON.parse(raw) as { user?: { role?: Role } }) : null
      const role = stored?.user?.role
      if (role && roles.includes(role)) {
        next()
        return
      }
    } catch {
      // Malformed stored state — fall through to 403
    }

    next({ path: '/app/403' })
  }
}
