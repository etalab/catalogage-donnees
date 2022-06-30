import { DATASET_FILTER_CATEGORIES } from "src/constants";
import type {
  SelectableDatasetFilterGroup,
  DatasetFilters,
  SelectableDatasetFilter,
} from "src/definitions/datasets";

export const mergeSelectableDatasetFilter = (
  source: Partial<SelectableDatasetFilter>,
  newFilters: Partial<SelectableDatasetFilter>
): Partial<SelectableDatasetFilter> => {
  return {
    ...source,
    ...newFilters,
  };
};

export const cleanSearchFilters = (
  selectedSearchFilter: Partial<SelectableDatasetFilter>
): Partial<SelectableDatasetFilter> => {
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

export const groupSelectableDatasetFilterByCategory = (
  filters: SelectableDatasetFilter
): SelectableDatasetFilterGroup => {
  const initialValues: SelectableDatasetFilterGroup = {
    "Informations Générales": {},
    "Sources et Formats": {},
    "Mots-clés Thématiques": {},
  };

  return Object.keys(DATASET_FILTER_CATEGORIES).reduce((previous, current) => {
    const filtersKey = DATASET_FILTER_CATEGORIES[current] as string[];

    const mappedFilterKeys = filtersKey.reduce((previous, current) => {
      return {
        ...previous,
        [current]: filters[current],
      };
    }, {}) as Partial<DatasetFilters>;

    return {
      ...previous,
      [current]: mappedFilterKeys,
    };
  }, initialValues);
};
