import { GEOGRAPHICAL_COVERAGE_LABELS } from "src/constants";
import type {
  SearchFilter,
  SelectableSearchFilter,
} from "src/definitions/datasets";
import { getFakeDataset } from "src/tests/factories/dataset";
import { buildFakeTag } from "src/tests/factories/tags";
import {
  toDataset,
  toPayload,
  camelToUnderscore,
  transformKeysToUnderscoreCase,
  transformSearchFiltersIntoSelectableSearchFilters,
} from "./dataset";

describe("transformers -- dataset", () => {
  test("transformKeysToUnderscoreCase", () => {
    const text = "helloWorld";
    const result = camelToUnderscore(text);
    expect(result).toBe("hello_world");
  });

  test("transformKeysToUnderscoreCase", () => {
    const input = {
      helloWorld: "hello",
      fooBaz: "hello",
    };
    const result = transformKeysToUnderscoreCase(input);

    expect(Object.keys(result).every((key) => key.includes("_"))).toBe(true);
  });

  test("toPayload", () => {
    const dataset = getFakeDataset();
    const result = toPayload(dataset);
    expect(Object.keys(result).every((key) => key === key.toLowerCase())).toBe(
      true
    );
  });

  test("toDataset", () => {
    const dataset = toPayload(getFakeDataset());
    const result = toDataset({
      ...dataset,
      catalog_record: { created_at: new Date().toISOString() },
    });
    expect(Object.keys(result).every((key) => key === key.toLowerCase())).toBe(
      false
    );
  });

  describe("transformAPISearchFiltersIntoSearchFilters", () => {
    test("should transform an SearchFilter into SelectableSearchFilter", () => {
      const tag1 = buildFakeTag({
        id: "xyz-555-666",
        name: "monTag",
      });

      const tag2 = buildFakeTag({
        id: "abc-111-2226",
        name: "monTag2",
      });

      const source: SearchFilter = {
        format: ["CSV", "XLS"],
        geographical_coverage: ["epci", "department"],
        service: ["DINUM"],
        tag_id: [tag1, tag2],
        technical_source: ["DINUM", "ADEME"],
      };

      const expectedResult: SelectableSearchFilter = {
        format: [
          { label: "CSV", value: "CSV" },
          { label: "XLS", value: "XLS" },
        ],
        geographical_coverage: [
          { label: GEOGRAPHICAL_COVERAGE_LABELS.epci, value: "epci" },
          {
            label: GEOGRAPHICAL_COVERAGE_LABELS.department,
            value: "department",
          },
        ],
        service: [{ label: "DINUM", value: "DINUM" }],
        tag_id: [
          { label: tag1.name, value: tag1.id },
          { label: tag2.name, value: tag2.id },
        ],
        technical_source: [
          {
            label: "DINUM",
            value: "DINUM",
          },
          {
            label: "ADEME",
            value: "ADEME",
          },
        ],
      };

      expect(transformSearchFiltersIntoSelectableSearchFilters(source)).toEqual(
        expectedResult
      );
    });
  });
});
