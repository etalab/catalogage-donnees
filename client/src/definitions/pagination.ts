export type GetPageLink = (page: number) => string;

export type Paginated<T = unknown> = {
  items: T[];
  totalItems: number;
  totalPages: number;
};
