export type Fetch = (request: Request) => Promise<Response>;

export type ApiResponse<T> = { status: number; data: T };
