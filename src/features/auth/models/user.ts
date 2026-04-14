import type { Role } from '@/core/config/constants'

export interface User {
  id: string
  email: string
  full_name: string
  role: Role
  created_at: string
}
