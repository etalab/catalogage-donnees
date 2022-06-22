import type { SearchFilter } from "src/definitions/searchFilters";

export const toSearchQueryParamRecord = (
  searchFilter: SearchFilter
): string[][] => {
  return Object.keys(searchFilter).reduce((previous, current) => {
    const value = searchFilter[current];

    if (value) {
      return [...previous, [current, ...value]];
    }

    return previous;
  }, []);
};
