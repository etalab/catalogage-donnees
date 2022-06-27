import { SEARCH_FILTERS_CATEGORIES } from "src/constants";
import type {
  FilterCategoryGroup,
  SearchFilter,
  SelectableSearchFilter,
} from "src/definitions/datasets";

export const mergeSelectableSearchFilter = (
  source: SelectableSearchFilter,
  newFilters: Partial<SelectableSearchFilter>
): SelectableSearchFilter => {
  return {
    ...source,
    ...newFilters,
  };
};

export const cleanSearchFilters = (
  selectedSearchFilter: SelectableSearchFilter
): Partial<SelectableSearchFilter> => {
  return Object.keys(selectedSearchFilter).reduce((previous, current) => {
    if (selectedSearchFilter[current]) {
      return {
        ...previous,
        [current]: selectedSearchFilter[current],
      };
    }
    return previous;
  }, {});
};

export const groupSelectableSearchFilterByCategory = (
  filters: SelectableSearchFilter
): FilterCategoryGroup => {
  const initialValues: FilterCategoryGroup = {
    "Informations Générales": {},
    "Sources et Formats": {},
    "Mots-clés Thématiques": {},
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
