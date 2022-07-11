import type {
  DatasetFiltersInfo,
  DatasetFiltersOptions,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import { toQueryString } from "../util/urls";
import {
  toFiltersOptions,
  toFiltersParams,
  toFiltersValue,
} from "./datasetFilters";

describe("transformers -- Dataset filters", () => {
  const info: DatasetFiltersInfo = {
    geographicalCoverage: ["epci", "department"],
    service: ["DINUM"],
    format: ["file_tabular", "file_gis"],
    technicalSource: ["Base centrale", "Serveur GIS"],
    tagId: [
      {
        id: "xyz-555-666",
        name: "monTag1",
      },
      {
        id: "abc-111-2226",
        name: "monTag2",
      },
    ],
  };

  const value: DatasetFiltersValue = {
    geographicalCoverage: "epci",
    format: "file_gis",
    service: null,
    technicalSource: "Serveur GIS",
    tagId: null,
  };

  test("toFiltersParams", () => {
    const params = [
      ["geographical_coverage", "epci"],
      ["service", null],
      ["format", "file_gis"],
      ["technical_source", "Serveur GIS"],
      ["tag_id", null],
    ];

    expect(toFiltersParams(value)).toEqual(params);
  });

  test("getFiltersValueFromParams", () => {
    const queryString = toQueryString(toFiltersParams(value));
    expect(queryString).toBe(
      "?geographical_coverage=epci&format=file_gis&technical_source=Serveur+GIS"
    );
    expect(toFiltersValue(new URLSearchParams(queryString))).toEqual(value);
  });

  test("toFiltersOptions", () => {
    const options: DatasetFiltersOptions = {
      geographicalCoverage: [
        { label: "EPCI", value: "epci" },
        { label: "Départementale", value: "department" },
      ],
      service: [{ label: "DINUM", value: "DINUM" }],
      format: [
        {
          label: "Fichier tabulaire (XLS, XLSX, CSV, ...)",
          value: "file_tabular",
        },
        { label: "Fichier SIG (Shapefile, ...)", value: "file_gis" },
      ],
      technicalSource: [
        { label: "Base centrale", value: "Base centrale" },
        { label: "Serveur GIS", value: "Serveur GIS" },
      ],
      tagId: [
        { label: "monTag1", value: "xyz-555-666" },
        { label: "monTag2", value: "abc-111-2226" },
      ],
    };

    expect(toFiltersOptions(info)).toEqual(options);
  });
});
