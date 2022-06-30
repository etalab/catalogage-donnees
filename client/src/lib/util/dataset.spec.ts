import { GEOGRAPHICAL_COVERAGE_LABELS } from "src/constants";
import type {
  SelectableDatasetFilterGroup,
  SelectableDatasetFilter,
} from "src/definitions/datasets";
import { getFakeSelectableDatasetFilter } from "src/tests/factories/dataset";
import { buildFakeTag } from "src/tests/factories/tags";
import {
  cleanSearchFilters,
  groupSelectableDatasetFilterByCategory,
  mergeSelectableDatasetFilter,
} from "./dataset";

describe("SearchFilters", () => {
  describe("cleanSearchFilters", () => {
    test("a search filter should not have null values", () => {
      const source: SelectableDatasetFilter = {
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

      const expectedResult: Partial<SelectableDatasetFilter> = {
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
  describe("mergeSelectableDatasetFilter", () => {
    test("should merge two searchFilters", () => {
      const tag1 = buildFakeTag({
        id: "foo",
        name: "bar",
      });
      const source = getFakeSelectableDatasetFilter({
        tag_id: [{ label: tag1.name, value: tag1.id }],
      });

      const newSearchFilter: Partial<SelectableDatasetFilter> = {
        service: [{ label: "DINUM", value: "DINUM" }],
      };

      const result = mergeSelectableDatasetFilter(source, newSearchFilter);

      expect(result.service).toEqual(newSearchFilter.service);
      expect(result.tag_id).toEqual(source.tag_id);
    });
  });

  describe("groupSearchFiltersByCategory", () => {
    test("should group filters by category", () => {
      const searchFilters = getFakeSelectableDatasetFilter({});

      const expectedResult: SelectableDatasetFilterGroup = {
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

      const result = groupSelectableDatasetFilterByCategory(searchFilters);
      expect(result).toEqual(expectedResult);
    });
  });
});