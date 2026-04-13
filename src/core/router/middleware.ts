import { router } from './index'

/**
 * Global navigation middleware
 */
router.beforeEach((_to, _from, next) => {
  // Future: auth checks, role validation, analytics tracking
  next()
})

export { router as routerWithMiddleware }
