/**
 * Standard API response types
 */

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface ApiError {
  status: number
  message: string
  detail?: string
  errors?: Record<string, string[]>
}

export interface Paginated<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}
