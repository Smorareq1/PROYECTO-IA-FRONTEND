/**
 * ─────────────────────────────────────────────────────────────────────────────
 * MOCK DATA TOGGLE
 * ─────────────────────────────────────────────────────────────────────────────
 * Cambia USE_MOCK a `false` cuando el backend FastAPI esté corriendo.
 * Nada más cambia — los servicios reales toman el control automáticamente.
 * ─────────────────────────────────────────────────────────────────────────────
 */
export const USE_MOCK = true

/** Simula latencia de red para que la UI se vea realista */
export const delay = (ms = 450) => new Promise<void>(resolve => setTimeout(resolve, ms))
