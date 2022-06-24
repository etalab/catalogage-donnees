import { SEARCH_FILTERS_CATEGORIES } from "src/constants";
import type {
  FilterCategoryGroup,
  SearchFilter,
} from "src/definitions/searchFilters";

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

export const groupSearchFiltersByCategory = (
  filters: SearchFilter
): FilterCategoryGroup => {
  const initialValues: FilterCategoryGroup = {
    "Informations Générales": {},
    "Mots-clés Thématiques": {},
    "Sources et Formats": {},
  };

  return Object.keys(SEARCH_FILTERS_CATEGORIES).reduce((previous, current) => {
    const filtersKey = SEARCH_FILTERS_CATEGORIES[current] as string[];

    const mappedFilterKeys = filtersKey.reduce((previous, current) => {
      return {
        ...previous,
        [current]: filters[current],
      };
    }, {}) as SearchFilter;

    return {
      ...previous,
      [current]: mappedFilterKeys,
    };
  }, initialValues);
};
