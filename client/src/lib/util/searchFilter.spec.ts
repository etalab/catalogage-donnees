import { GEOGRAPHICAL_COVERAGE_LABELS } from "src/constants";
import type {
  FilterCategoryGroup,
  SearchFilter,
} from "src/definitions/searchFilters";
import {
  cleanSearchFilters,
  groupSearchFiltersByCategory,
  mergeSearchFilters,
} from "./searchFilters";

describe("SearchFilters", () => {
  describe("cleanSearchFilters", () => {
    test("a search filter should not have null values", () => {
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
  });

  describe("groupSearchFiltersByCategory", () => {
    test("should group filters by category", () => {
      const searchFilters: SearchFilter = {
        tags: ["foo", "bar", "baz"],
        opening: ["restricted", "open"],
        service: ["DGSE", "DGSI"],
        geographical_coverage: [
          GEOGRAPHICAL_COVERAGE_LABELS.department,
          GEOGRAPHICAL_COVERAGE_LABELS.epci,
        ],
        format: ["Excel", "CSV"],
        technical_source: ["tata", "toto"],
      };

      const expectedResult: FilterCategoryGroup = {
        "Informations Générales": {
          opening: ["restricted", "open"],
          geographical_coverage: [
            GEOGRAPHICAL_COVERAGE_LABELS.department,
            GEOGRAPHICAL_COVERAGE_LABELS.epci,
          ],
          service: ["DGSE", "DGSI"],
        },
        "Mots-clés Thématiques": {
          tags: ["foo", "bar", "baz"],
        },

        "Sources et Formats": {
          format: ["Excel", "CSV"],
          technical_source: ["tata", "toto"],
        },
      };

      const result = groupSearchFiltersByCategory(searchFilters);

      expect(result).toEqual(expectedResult);
    });
  });
});
