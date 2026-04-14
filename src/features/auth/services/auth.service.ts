import { apiClient } from '@/core/api/client'
import type { User } from '../models/user'
import type { LoginCredentials } from '../models/credentials.schema'
import { setTokens, clearTokens } from '@/core/auth/token-storage'
import { USE_MOCK } from '@/mockupdata'
import * as mock from '@/mockupdata/services/auth.mock'

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  if (USE_MOCK) return mock.login(credentials)
  const { data } = await apiClient.post<AuthResponse>('/auth/login', credentials)
  setTokens(data.access_token, data.refresh_token)
  return data
}

export async function logout(): Promise<void> {
  if (USE_MOCK) return mock.logout()
  try {
    await apiClient.post('/auth/logout')
  } finally {
    clearTokens()
  }
}

export async function getMe(): Promise<User> {
  if (USE_MOCK) return mock.getMe()
  const { data } = await apiClient.get<User>('/auth/me')
  return data
}
