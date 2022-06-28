import type { SelectableSearchFilter } from "src/definitions/datasets";
import type { SelectOption } from "src/definitions/form";
import type { QueryParamRecord } from "src/definitions/url";

export const toSearchQueryParamRecord = (
  searchFilter: Partial<SelectableSearchFilter>
): QueryParamRecord => {
  return Object.keys(searchFilter).reduce((previous, current) => {
    const options: SelectOption[] = searchFilter[current];

    if (options) {
      const values = options.map((item) => item.value).filter((item) => item);
      return [...previous, [current, ...values]];
    }

    return previous;
  }, []) as unknown as QueryParamRecord;
};
