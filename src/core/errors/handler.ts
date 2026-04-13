import { useToast } from '@/core/composables/useToast'
import { HttpError } from './HttpError'
import { AppError } from './AppError'
import type { AxiosError } from 'axios'

/**
 * Global error handler — maps errors to user-friendly toast notifications
 */
export function handleError(error: unknown): void {
  const toast = useToast()

  if (error instanceof HttpError) {
    if (error.isUnauthorized) {
      toast.error('Sesión expirada', 'Por favor inicia sesión nuevamente.')
    } else if (error.isForbidden) {
      toast.error('Sin permisos', 'No tienes permiso para realizar esta acción.')
    } else if (error.isNotFound) {
      toast.error('No encontrado', 'El recurso solicitado no existe.')
    } else if (error.isServerError) {
      toast.error('Error del servidor', 'Ocurrió un error inesperado. Intenta de nuevo.')
    } else {
      toast.error('Error', error.message)
    }
    return
  }

  if (error instanceof AppError) {
    toast.error('Error', error.message)
    return
  }

  // Axios error
  if (isAxiosError(error)) {
    const status = error.response?.status ?? 0
    const message =
      (error.response?.data as { detail?: string })?.detail ??
      error.message ??
      'Error de conexión'
    toast.error(`Error ${status || 'de red'}`, message)
    return
  }

  // Unknown error
  console.error('Unhandled error:', error)
  toast.error('Error inesperado', 'Algo salió mal. Intenta de nuevo.')
}

function isAxiosError(error: unknown): error is AxiosError {
  return (error as AxiosError)?.isAxiosError === true
}
