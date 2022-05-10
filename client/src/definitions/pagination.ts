export type GetPageLink = (page: number) => string;

export type Paginated<T = unknown> = {
  items: T[];
  totalItems: number;
  pageSize: number;
  totalPages: number;
};
