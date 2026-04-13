import type { Role } from '@/core/config/constants'

/**
 * Permission map: role → allowed actions
 */
export const PERMISSIONS: Record<Role, string[]> = {
  cliente: [
    'ticket:create',
    'ticket:read:own',
  ],
  agente: [
    'ticket:read:all',
    'ticket:update',
    'ticket:assign',
    'classifier:use',
  ],
  admin: [
    'ticket:read:all',
    'ticket:update',
    'ticket:delete',
    'ticket:assign',
    'classifier:use',
    'analytics:read',
    'model:read',
    'user:manage',
  ],
}

/**
 * Check if a role has a specific permission
 */
export function hasPermission(role: Role, action: string): boolean {
  return PERMISSIONS[role]?.includes(action) ?? false
}
