import { delay } from '@/mockupdata'
import { MOCK_USERS, DEFAULT_MOCK_USER } from '@/mockupdata/data/auth.data'
import { setTokens } from '@/core/auth/token-storage'
import type { LoginCredentials } from '@/features/auth/models/credentials.schema'
import type { AuthResponse } from '@/features/auth/services/auth.service'
import type { User } from '@/features/auth/models/user'

export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  await delay()

  const sessionUser = MOCK_USERS[credentials.email] ?? DEFAULT_MOCK_USER

  const fakeToken = `mock_token_${sessionUser.role}_${Date.now()}`
  setTokens(fakeToken, `mock_refresh_${Date.now()}`)

  const user: User = {
    id: sessionUser.id,
    email: sessionUser.email,
    full_name: sessionUser.full_name,
    role: sessionUser.role,
    created_at: '2026-01-01T00:00:00Z',
  }

  return {
    access_token: fakeToken,
    refresh_token: `mock_refresh_${Date.now()}`,
    user,
  }
}

export async function logout(): Promise<void> {
  await delay(200)
}

export async function getMe(): Promise<User> {
  await delay(200)
  // Read role from stored token prefix (mock convention)
  const token = localStorage.getItem('ticket_ai_access_token') ?? ''
  const roleMatch = token.match(/mock_token_(\w+)_/)
  const role = (roleMatch?.[1] ?? 'admin') as User['role']

  const byRole = Object.values(MOCK_USERS).find(u => u.role === role) ?? DEFAULT_MOCK_USER

  return {
    id: byRole.id,
    email: byRole.email,
    full_name: byRole.full_name,
    role: byRole.role,
    created_at: '2026-01-01T00:00:00Z',
  }
}
