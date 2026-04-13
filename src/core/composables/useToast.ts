import { ref, readonly } from 'vue'

export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

const toasts = ref<Toast[]>([])
let toastId = 0

function addToast(toast: Omit<Toast, 'id'>) {
  const id = `toast-${++toastId}`
  const newToast: Toast = { ...toast, id }
  toasts.value.push(newToast)

  const duration = toast.duration ?? 5000
  if (duration > 0) {
    setTimeout(() => removeToast(id), duration)
  }
}

function removeToast(id: string) {
  toasts.value = toasts.value.filter((t) => t.id !== id)
}

/**
 * Global toast notification composable
 */
export function useToast() {
  return {
    toasts: readonly(toasts),
    addToast,
    removeToast,
    success: (title: string, message?: string) =>
      addToast({ type: 'success', title, message }),
    error: (title: string, message?: string) =>
      addToast({ type: 'error', title, message }),
    warning: (title: string, message?: string) =>
      addToast({ type: 'warning', title, message }),
    info: (title: string, message?: string) =>
      addToast({ type: 'info', title, message }),
  }
}
