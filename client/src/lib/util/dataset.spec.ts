import { GEOGRAPHICAL_COVERAGE_LABELS } from "src/constants";
import type {
  SelectableSearchFilterGroup,
  SelectableSearchFilter,
} from "src/definitions/datasets";
import { getFakeSelectableSearchFilter } from "src/tests/factories/dataset";
import { buildFakeTag } from "src/tests/factories/tags";
import {
  cleanSearchFilters,
  groupSelectableSearchFilterByCategory,
  mergeSelectableSearchFilter,
} from "./dataset";

describe("SearchFilters", () => {
  describe("cleanSearchFilters", () => {
    test("a search filter should not have null values", () => {
      const source: SelectableSearchFilter = {
        tag_id: null,
        geographical_coverage: [
          {
            label: GEOGRAPHICAL_COVERAGE_LABELS.epci,
            value: "epci",
          },
        ],
        service: [{ label: "DINUM", value: "DINUM" }],
        technical_source: [{ label: "foo", value: "foo" }],
        format: null,
      };

      const expectedResult: Partial<SelectableSearchFilter> = {
        geographical_coverage: [
          {
            label: GEOGRAPHICAL_COVERAGE_LABELS.epci,
            value: "epci",
          },
        ],
        service: [{ label: "DINUM", value: "DINUM" }],
        technical_source: [{ label: "foo", value: "foo" }],
      };
      const result = cleanSearchFilters(source);

      expect(result).toEqual(expectedResult);
    });
  });
  describe("mergeSelectableSearchFilter", () => {
    test("should merge two searchFilters", () => {
      const tag1 = buildFakeTag({
        id: "foo",
        name: "bar",
      });
      const source = getFakeSelectableSearchFilter({
        tag_id: [{ label: tag1.name, value: tag1.id }],
      });

      const newSearchFilter: Partial<SelectableSearchFilter> = {
        service: [{ label: "DINUM", value: "DINUM" }],
      };

      const result = mergeSelectableSearchFilter(source, newSearchFilter);

      expect(result.service).toEqual(newSearchFilter.service);
      expect(result.tag_id).toEqual(source.tag_id);
    });
  });

  describe("groupSearchFiltersByCategory", () => {
    test("should group filters by category", () => {
      const searchFilters = getFakeSelectableSearchFilter({});

      const expectedResult: SelectableSearchFilterGroup = {
        "Informations Générales": {
          geographical_coverage: searchFilters.geographical_coverage,
          service: searchFilters.service,
        },
        "Mots-clés Thématiques": {
          tag_id: searchFilters.tag_id,
        },

        "Sources et Formats": {
          format: searchFilters.format,
          technical_source: searchFilters.technical_source,
        },
      };

      const result = groupSelectableSearchFilterByCategory(searchFilters);
      expect(result).toEqual(expectedResult);
    });
  });
});
