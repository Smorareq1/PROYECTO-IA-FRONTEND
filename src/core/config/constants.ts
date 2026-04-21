/**
 * Application-wide constants
 * Categories match the Bitext Customer Support dataset (11 classes)
 */

export const CATEGORIES = [
  'ACCOUNT',
  'CANCEL',
  'CONTACT',
  'DELIVERY',
  'FEEDBACK',
  'INVOICE',
  'ORDER',
  'PAYMENT',
  'REFUND',
  'SHIPPING',
  'SUBSCRIPTION',
] as const

export type Category = typeof CATEGORIES[number]

export const CATEGORY_LABELS: Record<Category, string> = {
  ACCOUNT:      'Cuenta',
  CANCEL:       'Cancelación',
  CONTACT:      'Contacto',
  DELIVERY:     'Entrega',
  FEEDBACK:     'Retroalimentación',
  INVOICE:      'Facturación',
  ORDER:        'Órdenes',
  PAYMENT:      'Pagos',
  REFUND:       'Reembolsos',
  SHIPPING:     'Envíos',
  SUBSCRIPTION: 'Suscripción',
}

export const CATEGORY_COLORS: Record<Category, { text: string; bg: string; css: string }> = {
  ACCOUNT:      { text: 'var(--ds-cat-account)',      bg: 'var(--ds-cat-account-bg)',      css: 'cat-account' },
  CANCEL:       { text: 'var(--ds-cat-cancel)',       bg: 'var(--ds-cat-cancel-bg)',       css: 'cat-cancel' },
  CONTACT:      { text: 'var(--ds-cat-contact)',      bg: 'var(--ds-cat-contact-bg)',      css: 'cat-contact' },
  DELIVERY:     { text: 'var(--ds-cat-delivery)',     bg: 'var(--ds-cat-delivery-bg)',     css: 'cat-delivery' },
  FEEDBACK:     { text: 'var(--ds-cat-feedback)',     bg: 'var(--ds-cat-feedback-bg)',     css: 'cat-feedback' },
  INVOICE:      { text: 'var(--ds-cat-invoice)',      bg: 'var(--ds-cat-invoice-bg)',      css: 'cat-invoice' },
  ORDER:        { text: 'var(--ds-cat-order)',        bg: 'var(--ds-cat-order-bg)',        css: 'cat-order' },
  PAYMENT:      { text: 'var(--ds-cat-payment)',      bg: 'var(--ds-cat-payment-bg)',      css: 'cat-payment' },
  REFUND:       { text: 'var(--ds-cat-refund)',       bg: 'var(--ds-cat-refund-bg)',       css: 'cat-refund' },
  SHIPPING:     { text: 'var(--ds-cat-shipping)',     bg: 'var(--ds-cat-shipping-bg)',     css: 'cat-shipping' },
  SUBSCRIPTION: { text: 'var(--ds-cat-subscription)', bg: 'var(--ds-cat-subscription-bg)', css: 'cat-subscription' },
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
