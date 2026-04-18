import type { ModelInfo, ModelMetrics, ConfusionMatrix, TopWord } from '@/features/metrics/models/metrics'
import type { KFoldReport } from '@/features/metrics/models/kfold'
import type { Category } from '@/core/config/constants'

export const MOCK_MODEL_INFO: ModelInfo = {
  version: '1.4.2',
  trained_at: '2026-04-08T03:00:00Z',
  vocab_size: 4_817,
  doc_count: 500,
  classes: ['soporte_tecnico', 'facturacion', 'consulta_general', 'queja', 'cancelacion'],
}

export const MOCK_METRICS: ModelMetrics = {
  accuracy: 0.892,
  macro_f1: 0.879,
  per_class: [
    { class: 'soporte_tecnico',  precision: 0.912, recall: 0.900, f1: 0.906, support: 100 },
    { class: 'facturacion',      precision: 0.930, recall: 0.905, f1: 0.917, support: 95  },
    { class: 'consulta_general', precision: 0.844, recall: 0.875, f1: 0.859, support: 120 },
    { class: 'queja',            precision: 0.876, recall: 0.867, f1: 0.871, support: 105 },
    { class: 'cancelacion',      precision: 0.920, recall: 0.925, f1: 0.922, support: 80  },
  ],
}

export const MOCK_CONFUSION_MATRIX: ConfusionMatrix = {
  labels: ['soporte_tecnico', 'facturacion', 'consulta_general', 'queja', 'cancelacion'],
  //        pred →  sop  fac  con  que  can
  matrix: [
    [90,  2,  5,  2,  1],   // real: soporte_tecnico  (total 100)
    [ 2, 86,  3,  2,  2],   // real: facturacion      (total 95)
    [ 7,  3, 105,  4,  1],  // real: consulta_general (total 120)
    [ 4,  2,  6,  91,  2],  // real: queja            (total 105)
    [ 1,  2,  1,  2,  74],  // real: cancelacion      (total 80)
  ],
}

export const MOCK_KFOLDS: KFoldReport = {
  k: 5,
  folds: [
    {
      fold: 1, accuracy: 0.875, macro_f1: 0.861,
      per_class: MOCK_METRICS.per_class.map(m => ({ ...m, f1: m.f1 - 0.015 })),
    },
    {
      fold: 2, accuracy: 0.910, macro_f1: 0.897,
      per_class: MOCK_METRICS.per_class.map(m => ({ ...m, f1: m.f1 + 0.018 })),
    },
    {
      fold: 3, accuracy: 0.892, macro_f1: 0.879,
      per_class: MOCK_METRICS.per_class,
    },
    {
      fold: 4, accuracy: 0.885, macro_f1: 0.872,
      per_class: MOCK_METRICS.per_class.map(m => ({ ...m, f1: m.f1 - 0.007 })),
    },
    {
      fold: 5, accuracy: 0.898, macro_f1: 0.886,
      per_class: MOCK_METRICS.per_class.map(m => ({ ...m, f1: m.f1 + 0.007 })),
    },
  ],
  mean: { accuracy: 0.892, macro_f1: 0.879 },
  std:  { accuracy: 0.013, macro_f1: 0.013 },
}

export const MOCK_TOP_WORDS: Record<Category, TopWord[]> = {
  soporte_tecnico: [
    { word: 'error',        weight: 4.21 },
    { word: 'acceso',       weight: 3.87 },
    { word: 'contraseña',   weight: 3.74 },
    { word: 'sistema',      weight: 3.51 },
    { word: 'configurar',   weight: 3.42 },
    { word: 'instalar',     weight: 3.38 },
    { word: 'pantalla',     weight: 3.20 },
    { word: 'dispositivo',  weight: 3.14 },
    { word: 'técnico',      weight: 3.09 },
    { word: 'actualizar',   weight: 2.98 },
    { word: 'conexión',     weight: 2.87 },
    { word: 'reiniciar',    weight: 2.76 },
    { word: 'red',          weight: 2.65 },
    { word: 'soporte',      weight: 2.54 },
    { word: 'fallo',        weight: 2.43 },
  ],
  facturacion: [
    { word: 'factura',      weight: 4.55 },
    { word: 'cobro',        weight: 4.32 },
    { word: 'cargo',        weight: 4.18 },
    { word: 'reembolso',    weight: 4.05 },
    { word: 'pago',         weight: 3.91 },
    { word: 'tarjeta',      weight: 3.77 },
    { word: 'débito',       weight: 3.63 },
    { word: 'mensual',      weight: 3.49 },
    { word: 'suscripción',  weight: 3.35 },
    { word: 'precio',       weight: 3.21 },
    { word: 'recibo',       weight: 3.07 },
    { word: 'importe',      weight: 2.93 },
    { word: 'doble',        weight: 2.79 },
    { word: 'monto',        weight: 2.65 },
    { word: 'cobraron',     weight: 2.51 },
  ],
  consulta_general: [
    { word: 'información',  weight: 3.92 },
    { word: 'horario',      weight: 3.78 },
    { word: 'consulta',     weight: 3.64 },
    { word: 'disponible',   weight: 3.50 },
    { word: 'proceso',      weight: 3.36 },
    { word: 'servicio',     weight: 3.22 },
    { word: 'solicitar',    weight: 3.08 },
    { word: 'ayuda',        weight: 2.94 },
    { word: 'detalles',     weight: 2.80 },
    { word: 'conocer',      weight: 2.66 },
    { word: 'cuándo',       weight: 2.52 },
    { word: 'dónde',        weight: 2.38 },
    { word: 'procedimiento',weight: 2.24 },
    { word: 'tiempo',       weight: 2.10 },
    { word: 'cómo',         weight: 1.96 },
  ],
  queja: [
    { word: 'insatisfecho', weight: 4.78 },
    { word: 'inaceptable',  weight: 4.61 },
    { word: 'deficiente',   weight: 4.44 },
    { word: 'pésimo',       weight: 4.27 },
    { word: 'reclamación',  weight: 4.10 },
    { word: 'decepcionado', weight: 3.93 },
    { word: 'terrible',     weight: 3.76 },
    { word: 'demora',       weight: 3.59 },
    { word: 'tardanza',     weight: 3.42 },
    { word: 'queja',        weight: 3.25 },
    { word: 'gestión',      weight: 3.08 },
    { word: 'respuesta',    weight: 2.91 },
    { word: 'calidad',      weight: 2.74 },
    { word: 'incumplimiento',weight: 2.57 },
    { word: 'exijo',        weight: 2.40 },
  ],
  cancelacion: [
    { word: 'cancelar',     weight: 5.12 },
    { word: 'baja',         weight: 4.89 },
    { word: 'finalizar',    weight: 4.66 },
    { word: 'terminar',     weight: 4.43 },
    { word: 'desactivar',   weight: 4.20 },
    { word: 'cancelación',  weight: 3.97 },
    { word: 'cerrar',       weight: 3.74 },
    { word: 'suspender',    weight: 3.51 },
    { word: 'contrato',     weight: 3.28 },
    { word: 'definitivo',   weight: 3.05 },
    { word: 'darme',        weight: 2.82 },
    { word: 'dejar',        weight: 2.59 },
    { word: 'fin',          weight: 2.36 },
    { word: 'plan',         weight: 2.13 },
    { word: 'último',       weight: 1.90 },
  ],
}
