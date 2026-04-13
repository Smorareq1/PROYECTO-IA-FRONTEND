/**
 * Application-wide constants
 */

export const CATEGORIES = [
  'soporte_tecnico',
  'facturacion',
  'consulta_general',
  'queja',
  'cancelacion',
] as const

export type Category = typeof CATEGORIES[number]

export const CATEGORY_LABELS: Record<Category, string> = {
  soporte_tecnico: 'Soporte Técnico',
  facturacion: 'Facturación',
  consulta_general: 'Consulta General',
  queja: 'Queja',
  cancelacion: 'Cancelación',
}

export const CATEGORY_COLORS: Record<Category, { text: string; bg: string; css: string }> = {
  soporte_tecnico:  { text: 'var(--ds-cat-soporte)',      bg: 'var(--ds-cat-soporte-bg)',      css: 'cat-soporte' },
  facturacion:      { text: 'var(--ds-cat-facturacion)',   bg: 'var(--ds-cat-facturacion-bg)',  css: 'cat-facturacion' },
  consulta_general: { text: 'var(--ds-cat-consulta)',      bg: 'var(--ds-cat-consulta-bg)',     css: 'cat-consulta' },
  queja:            { text: 'var(--ds-cat-queja)',         bg: 'var(--ds-cat-queja-bg)',        css: 'cat-queja' },
  cancelacion:      { text: 'var(--ds-cat-cancelacion)',   bg: 'var(--ds-cat-cancelacion-bg)',  css: 'cat-cancelacion' },
}

export const TICKET_STATUSES = ['abierto', 'en_progreso', 'resuelto', 'cerrado'] as const
export type TicketStatus = typeof TICKET_STATUSES[number]

export const STATUS_LABELS: Record<TicketStatus, string> = {
  abierto: 'Abierto',
  en_progreso: 'En Progreso',
  resuelto: 'Resuelto',
  cerrado: 'Cerrado',
}

export const ROLES = ['cliente', 'agente', 'admin'] as const
export type Role = typeof ROLES[number]

export const ROLE_LABELS: Record<Role, string> = {
  cliente: 'Cliente',
  agente: 'Agente',
  admin: 'Administrador',
}
