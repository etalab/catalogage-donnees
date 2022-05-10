export type Fetch = (request: Request) => Promise<Response>;

export type ApiResponse<T> = { status: number; data: T };

export type ApiPagination<T = unknown> = {
  items: T[];
  total_items: number;
  page_size: number;
};
