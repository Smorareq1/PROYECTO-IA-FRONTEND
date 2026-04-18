import { router } from './index'

router.beforeEach((_to, _from, next) => {
  next()
})

export { router as routerWithMiddleware }
