import type { Paginated } from "src/definitions/pagination";

type ApiPaginatedData<T> = {
  items: T[];
  total_items: number;
  total_pages: number;
};

export const toPaginated = <I, T>(
  data: ApiPaginatedData<I>,
  mapItem: (item: I) => T = (item) => item as unknown as T
): Paginated<T> => {
  const { items, total_items, total_pages } = data;

  return {
    items: items.map((item) => mapItem(item)),
    totalItems: total_items,
    totalPages: total_pages,
  };
};
