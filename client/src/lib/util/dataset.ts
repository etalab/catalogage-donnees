import type { SelectableDatasetFilter } from "src/definitions/datasets";

export const mergeSelectableDatasetFilter = (
  source: Partial<SelectableDatasetFilter>,
  newFilters: Partial<SelectableDatasetFilter>
): Partial<SelectableDatasetFilter> => {
  return {
    ...source,
    ...newFilters,
  };
};

export const cleanSearchDatasetFilters = (
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
