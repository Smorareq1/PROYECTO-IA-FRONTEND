import { format, formatDistanceToNow, parseISO } from 'date-fns'
import { es } from 'date-fns/locale'

/**
 * Format a date string to a human-readable format
 */
export function formatDate(dateStr: string, pattern = 'dd MMM yyyy'): string {
  try {
    return format(parseISO(dateStr), pattern, { locale: es })
  } catch {
    return dateStr
  }
}

/**
 * Format a date string to a relative time (e.g., "hace 2 horas")
 */
export function formatRelativeTime(dateStr: string): string {
  try {
    return formatDistanceToNow(parseISO(dateStr), { addSuffix: true, locale: es })
  } catch {
    return dateStr
  }
}

/**
 * Format a number as percentage
 */
export function formatPercent(value: number, decimals = 1): string {
  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength).trimEnd() + '…'
}

/**
 * Format milliseconds for display
 */
export function formatMs(ms: number): string {
  if (ms < 1000) return `${ms.toFixed(0)}ms`
  return `${(ms / 1000).toFixed(2)}s`
}
