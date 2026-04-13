import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Merge Tailwind CSS classes with clsx + tailwind-merge
 * Prevents class conflicts and enables conditional classes
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs))
}
