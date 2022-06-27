import type { SelectableSearchFilter } from "src/definitions/datasets";
import { buildFakeTag } from "src/tests/factories/tags";
import type { Maybe } from "../util/maybe";
import { toSearchQueryParamRecord } from "./searchFilter";

describe("Search Filters", () => {
  describe("toSearchQueryParamRecord", () => {
    it("should transform a searchFilter to a QueryParamRecord", () => {
      const tag1 = buildFakeTag();
      const searchFilter: Partial<SelectableSearchFilter> = {
        tags: [
          {
            label: tag1.name,
            value: tag1.id,
          },
        ],

        service: [
          {
            label: "DINUM",
            value: "DINUM",
          },
        ],
      };

      const expectedResult: [string, Maybe<string>][] = [
        ["tags", tag1.id],
        ["service", "DINUM"],
      ];
      const result = toSearchQueryParamRecord(searchFilter);

      expect(result).toEqual(expectedResult);
    });
  });
});
