import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import type { Role } from '@/core/config/constants'

export function requireAuth(
  _to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  next: NavigationGuardNext,
) {
  next()
}

export function requireRole(..._roles: Role[]) {
  return (
    _to: RouteLocationNormalized,
    _from: RouteLocationNormalized,
    next: NavigationGuardNext,
  ) => {
    next()
  }
}
