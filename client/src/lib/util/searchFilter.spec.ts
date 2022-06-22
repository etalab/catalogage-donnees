import type { SearchFilter } from "src/definitions/searchFilters";
import { cleanSearchFilters, mergeSearchFilters } from "./searchFilters";

describe("SearchFilters", () => {
  describe("cleanSearchFilters", () => {
    test.only("a search filter should not have null values", () => {
      const source: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
        tags: null,
      };

      const expectedResult: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
      };

      const result = cleanSearchFilters(source);

      expect(result).toEqual(expectedResult);
    });
  });
  describe("mergeSearchFilters", () => {
    test("should merge two searchFilters", () => {
      const source: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
      };

      const newSearchFilter: SearchFilter = {
        tags: ["new", "old", "present"],
      };
      const expectedResult: SearchFilter = {
        ...source,
        ...newSearchFilter,
      };

      const result = mergeSearchFilters(source, newSearchFilter);

      expect(result).toEqual(expectedResult);
    });

    test("should remove a filter if he was removed", () => {
      const source: SearchFilter = {
        tags: ["new", "old", "present"],
      };

      const newSearchFilter: SearchFilter = {
        tags: ["new", "present"],
      };
      const expectedResult: SearchFilter = {
        tags: ["new", "present"],
      };

      const result = mergeSearchFilters(source, newSearchFilter);

      expect(result).toEqual(expectedResult);
    });

    test("should remove a filter if he was removed AND should keep the untouched filters", () => {
      const source: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
        tags: ["new", "old", "present"],
      };

      const newSearchFilter: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
        tags: ["new", "present"],
      };
      const expectedResult: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
        tags: ["new", "present"],
      };

      const result = mergeSearchFilters(source, newSearchFilter);

      expect(result).toEqual(expectedResult);
    });

    test("new filters should not have null values", () => {
      const source: SearchFilter = {
        service: ["DINUM", "DGSE", "ETALAB"],
        tags: ["new", "old", "present"],
      };

      const newSearchFilter: SearchFilter = {
        service: null,
        tags: ["new", "present"],
      };

      const expectedResult: SearchFilter = {
        tags: ["new", "present"],
      };

      const result = mergeSearchFilters(source, newSearchFilter);

      expect(result).toEqual(expectedResult);
    });
  });
});
