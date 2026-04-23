// @ts-nocheck — Mock data is dead code (USE_MOCK=false). Categories no longer match real dataset.
import { delay } from '@/mockupdata'
import { MOCK_TICKETS } from '@/mockupdata/data/tickets.data'
import type { Ticket, CreateTicketDto, UpdateTicketDto } from '@/features/tickets/models/ticket'
import type { TicketFilters } from '@/features/tickets/services/tickets.service'
import type { Paginated } from '@/core/api/types'
import type { Category } from '@/core/config/constants'

// In-memory mutable copy so create/update/delete reflect in the session
let _tickets: Ticket[] = structuredClone(MOCK_TICKETS)

/** Naïve keyword-based categoriser for new tickets */
function guessCategory(text: string): { category: Category; confidences: Record<Category, number> } {
  const t = text.toLowerCase()

  const scores: Record<Category, number> = {
    soporte_tecnico:  [/error|acceso|contraseña|instalar|configurar|sistema|dispositivo|red|pantalla/].filter(r => r.test(t)).length * 2 +
                      (t.match(/\b(error|fallo|no funciona|problema técnico)\b/g)?.length ?? 0),
    facturacion:      [/factura|cobro|cargo|reembolso|pago|tarjeta|débito|suscripción|precio|recibo/].filter(r => r.test(t)).length * 2,
    consulta_general: [/información|horario|consulta|disponible|proceso|servicio|ayuda|cuándo|cómo/].filter(r => r.test(t)).length * 2,
    queja:            [/insatisfecho|inaceptable|deficiente|pésimo|reclamación|terrible|demora|queja/].filter(r => r.test(t)).length * 2,
    cancelacion:      [/cancelar|baja|finalizar|terminar|desactivar|cerrar|suspender|contrato/].filter(r => r.test(t)).length * 2,
  }

  // Ensure every category has at least a small noise value
  const cats = Object.keys(scores) as Category[]
  cats.forEach(c => { if (scores[c] === 0) scores[c] = Math.random() * 0.5 })

  const total = cats.reduce((s, c) => s + scores[c], 0)
  const confidences = {} as Record<Category, number>
  cats.forEach(c => { confidences[c] = parseFloat((scores[c] / total).toFixed(3)) })

  // Normalise so they sum to 1.0 exactly
  const sum = cats.reduce((s, c) => s + confidences[c], 0)
  confidences[cats[0]] += parseFloat((1 - sum).toFixed(3))

  const category = cats.reduce((best, c) => (confidences[c] > confidences[best] ? c : best), cats[0])
  return { category, confidences }
}

export async function getTickets(filters: TicketFilters = {}): Promise<Paginated<Ticket>> {
  await delay()

  let items = [..._tickets]

  if (filters.status)   items = items.filter(t => t.status === filters.status)
  if (filters.category) items = items.filter(t => (t.final_category ?? t.predicted_category) === filters.category)
  if (filters.assignee) items = items.filter(t => t.assignee_id === filters.assignee)
  if (filters.q) {
    const q = filters.q.toLowerCase()
    items = items.filter(t =>
      t.subject.toLowerCase().includes(q) ||
      t.description.toLowerCase().includes(q) ||
      t.id.toLowerCase().includes(q),
    )
  }

  // Sort newest first
  items.sort((a, b) => b.created_at.localeCompare(a.created_at))

  const page = filters.page ?? 1
  const size = filters.size ?? 20
  const start = (page - 1) * size

  return {
    items: items.slice(start, start + size),
    total: items.length,
    page,
    size,
    pages: Math.ceil(items.length / size),
  }
}

export async function getTicket(id: string): Promise<Ticket> {
  await delay(250)
  const ticket = _tickets.find(t => t.id === id)
  if (!ticket) throw new Error(`Ticket ${id} not found`)
  return structuredClone(ticket)
}

export async function createTicket(dto: CreateTicketDto): Promise<Ticket> {
  await delay(700)

  const { category, confidences } = guessCategory(`${dto.subject} ${dto.description}`)
  const now = new Date().toISOString()
  const padded = String(_tickets.length + 1).padStart(6, '0')

  const ticket: Ticket = {
    id: `TK-${padded}`,
    subject: dto.subject,
    description: dto.description,
    predicted_category: category,
    confidences,
    final_category: null,
    status: 'abierto',
    created_by: 'cliente@demo.com',
    assignee_id: null,
    created_at: now,
    updated_at: now,
  }

  _tickets.unshift(ticket)
  return structuredClone(ticket)
}

export async function updateTicket(id: string, dto: UpdateTicketDto): Promise<Ticket> {
  await delay(400)

  const idx = _tickets.findIndex(t => t.id === id)
  if (idx === -1) throw new Error(`Ticket ${id} not found`)

  _tickets[idx] = {
    ..._tickets[idx],
    ...dto,
    updated_at: new Date().toISOString(),
  }

  return structuredClone(_tickets[idx])
}

export async function deleteTicket(id: string): Promise<void> {
  await delay(400)
  _tickets = _tickets.filter(t => t.id !== id)
}
