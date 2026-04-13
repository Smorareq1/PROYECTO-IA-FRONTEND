import { AppError } from './AppError'

/**
 * HTTP-specific error with status code
 */
export class HttpError extends AppError {
  constructor(
    public readonly status: number,
    message: string,
    public readonly detail?: string,
  ) {
    super(message, `HTTP_${status}`)
    this.name = 'HttpError'
  }

  get isUnauthorized(): boolean {
    return this.status === 401
  }

  get isForbidden(): boolean {
    return this.status === 403
  }

  get isNotFound(): boolean {
    return this.status === 404
  }

  get isServerError(): boolean {
    return this.status >= 500
  }
}
