import axios from 'axios'
import { env } from '@/core/config/env'

/**
 * Axios instance with base configuration
 */
export const apiClient = axios.create({
  baseURL: env.VITE_API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})
