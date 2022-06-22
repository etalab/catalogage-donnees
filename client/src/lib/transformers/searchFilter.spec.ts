import { toSearchQueryParamRecord } from "./searchFilter";

describe("Search Filters", () => {
  describe("toSearchQueryParamRecord", () => {
    it("should transform a searchFilter to a QueryParamRecord", () => {
      const searchFilter = {
        tags: ["active", "night"],
        service: ["DGSE", "TATA"],
      };

      const expectedResult = [
        ["tags", "active", "night"],
        ["service", "DGSE", "TATA"],
      ];
      const result = toSearchQueryParamRecord(searchFilter);

      expect(result).toEqual(expectedResult);
    });
  });
});
