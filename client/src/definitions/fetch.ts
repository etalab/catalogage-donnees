export type Fetch = (request: Request) => Promise<Response>;

export type ApiResponse<T> = T extends void
  ? { status: number }
  : { status: number; data: T };
