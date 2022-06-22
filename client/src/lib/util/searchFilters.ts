import type { SearchFilter } from "src/definitions/searchFilters";

export const mergeSearchFilters = (
  source: SearchFilter,
  newFilters: SearchFilter
): SearchFilter => {
  return {
    ...source,
    ...newFilters,
  };
};

export const cleanSearchFilters = (
  searchFilter: SearchFilter
): SearchFilter => {
  return Object.keys(searchFilter).reduce((previous, current) => {
    if (searchFilter[current]) {
      return {
        ...previous,
        [current]: searchFilter[current],
      };
    }
    return previous;
  }, {}) as unknown as SearchFilter;
};
