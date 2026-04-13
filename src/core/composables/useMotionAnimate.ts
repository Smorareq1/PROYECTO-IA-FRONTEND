/**
 * Typed wrappers around the `motion` vanilla-DOM API.
 *
 * After each animation completes, we explicitly set the final
 * values as inline styles so they persist (motion's WAAPI backend
 * uses fill:"none" by default, which reverts styles on completion).
 */
import {
  animate as _animate,
  inView as _inView,
  stagger,
  type DOMKeyframesDefinition,
  type AnimationOptions as MotionAnimationOptions,
} from 'motion'

export { stagger }

export type Keyframes = DOMKeyframesDefinition

/** Extended options that accept both `ease` and `easing` */
export type AnimationOptions = MotionAnimationOptions & {
  easing?: readonly number[] | string | number[]
}

/** Mirror of motion's InViewOptions (not exported as a type) */
interface InViewOptions {
  root?: Element | Document
  margin?: string
  amount?: 'some' | 'all' | number
}

function normalizeOptions(opts?: AnimationOptions): MotionAnimationOptions | undefined {
  if (!opts) return undefined
  if ('easing' in opts && opts.easing && !('ease' in opts)) {
    const { easing, ...rest } = opts
    return { ...rest, ease: easing as MotionAnimationOptions['ease'] } as MotionAnimationOptions
  }
  return opts as MotionAnimationOptions
}

/**
 * Extract the final value from a keyframe definition.
 * Keyframes can be a single value or an array — we want the last one.
 */
function getFinalValue(v: unknown): string | number | undefined {
  if (Array.isArray(v)) return v[v.length - 1] as string | number
  return v as string | number | undefined
}

/**
 * After animation completes, persist final keyframe values
 * as inline styles on the element so they don't revert.
 */
function persistFinalStyles(el: Element, keyframes: DOMKeyframesDefinition) {
  if (!(el instanceof HTMLElement)) return
  for (const [prop, value] of Object.entries(keyframes)) {
    const final = getFinalValue(value)
    if (final === undefined) continue

    // Map motion shorthand props to CSS
    if (prop === 'x') {
      el.style.transform = el.style.transform.replace(/translateX\([^)]*\)/g, '').trim()
      el.style.transform += ` translateX(${typeof final === 'number' ? final + 'px' : final})`
      el.style.transform = el.style.transform.trim()
    } else if (prop === 'y') {
      el.style.transform = el.style.transform.replace(/translateY\([^)]*\)/g, '').trim()
      el.style.transform += ` translateY(${typeof final === 'number' ? final + 'px' : final})`
      el.style.transform = el.style.transform.trim()
    } else if (prop === 'scale') {
      el.style.transform = el.style.transform.replace(/scale\([^)]*\)/g, '').trim()
      el.style.transform += ` scale(${final})`
      el.style.transform = el.style.transform.trim()
    } else if (prop === 'opacity') {
      el.style.opacity = String(final)
    } else if (prop === 'width') {
      el.style.width = typeof final === 'number' ? final + 'px' : String(final)
    }
  }
  // Clean up transform if all values are identity
  if (el.style.transform) {
    el.style.transform = el.style.transform
      .replace(/translateX\(0px\)/g, '')
      .replace(/translateY\(0px\)/g, '')
      .replace(/scale\(1\)/g, '')
      .trim()
    if (!el.style.transform) el.style.removeProperty('transform')
  }
}

/**
 * Animate a single DOM element.
 */
export function animEl(
  el: Element | HTMLElement | null | undefined,
  keyframes: DOMKeyframesDefinition,
  options?: AnimationOptions,
) {
  if (!el) return
  const controls = _animate(el as unknown as string, keyframes, normalizeOptions(options))

  // Persist final styles after animation completes
  if (controls && typeof controls.then === 'function') {
    controls.then(() => persistFinalStyles(el, keyframes))
  } else {
    // Fallback: persist immediately if no promise
    persistFinalStyles(el, keyframes)
  }

  return controls
}

/**
 * Animate a NodeList / Element[] — the stagger-friendly variant.
 */
export function animList(
  list: NodeListOf<Element> | Element[],
  keyframes: DOMKeyframesDefinition,
  options?: AnimationOptions,
) {
  const controls = _animate(list as unknown as string, keyframes, normalizeOptions(options))

  // Persist final styles on all elements after animation completes
  if (controls && typeof controls.then === 'function') {
    controls.then(() => {
      const items = Array.from(list)
      items.forEach((el) => persistFinalStyles(el, keyframes))
    })
  }

  return controls
}

/**
 * inView — trigger a callback when `element` scrolls into view.
 */
export function inView(
  element: Element,
  onEnter: () => void,
  options?: InViewOptions,
) {
  return _inView(element as unknown as string, onEnter, options as Parameters<typeof _inView>[2])
}
