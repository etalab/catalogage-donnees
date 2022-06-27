import type { SelectableSearchFilter } from "src/definitions/datasets";
import type { SelectOption } from "src/definitions/form";
import type { Maybe } from "../util/maybe";

export const toSearchQueryParamRecord = (
  searchFilter: Partial<SelectableSearchFilter>
): [string, Maybe<string>][] => {
  return Object.keys(searchFilter).reduce((previous, current) => {
    const options: SelectOption[] = searchFilter[current];

    if (options) {
      const values = options.map((item) => item.value).filter((item) => item);
      return [...previous, [current, ...values]];
    }

    return previous;
  }, []) as unknown as [string, Maybe<string>][];
};
