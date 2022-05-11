import type { Paginated } from "src/definitions/pagination";

export const toPaginated = <T>(
  data: any,
  mapItem: (item: any) => T
): Paginated<T> => {
  const { items, total_items, total_pages } = data;

  return {
    items: items.map((item) => mapItem(item)),
    totalItems: total_items,
    totalPages: total_pages,
  };
};
