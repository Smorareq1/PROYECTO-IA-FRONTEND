import type { SessionUser } from '@/core/stores/auth.store'

/**
 * Usuarios de prueba.
 * Login con cualquier contraseña — el email determina el rol.
 * Emails no listados aquí → se loguean como admin por defecto.
 */
export const MOCK_USERS: Record<string, SessionUser> = {
  'admin@demo.com': {
    id: 'u-001',
    email: 'admin@demo.com',
    full_name: 'Admin Demo',
    role: 'admin',
  },
  'agente@demo.com': {
    id: 'u-002',
    email: 'agente@demo.com',
    full_name: 'Agente Demo',
    role: 'agente',
  },
  'cliente@demo.com': {
    id: 'u-003',
    email: 'cliente@demo.com',
    full_name: 'Cliente Demo',
    role: 'cliente',
  },
}

export const DEFAULT_MOCK_USER: SessionUser = MOCK_USERS['admin@demo.com']!
