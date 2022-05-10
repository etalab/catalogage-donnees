import type { Paginated } from "src/definitions/pagination";

export const toPaginated = <T>(
  data: any,
  mapItem: (item: any) => T
): Paginated<T> => {
  const { items, total_items, page_size, total_pages } = data;

  return {
    items: items.map((item) => mapItem(item)),
    totalItems: total_items,
    pageSize: page_size,
    totalPages: total_pages,
  };
};
