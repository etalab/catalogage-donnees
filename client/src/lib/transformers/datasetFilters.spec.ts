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
    geographicalCoverage: [
      "Métropole Européenne de Lille",
      "France métropolitaine",
    ],
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
    license: ["*", "Licence Ouverte"],
  };

  const value: DatasetFiltersValue = {
    geographicalCoverage: "France métropolitaine",
    format: "file_gis",
    service: null,
    technicalSource: "Serveur GIS",
    tagId: null,
    license: "Licence Ouverte",
  };

  test("toFiltersParams", () => {
    const params = [
      ["geographical_coverage", "France métropolitaine"],
      ["service", null],
      ["format", "file_gis"],
      ["technical_source", "Serveur GIS"],
      ["tag_id", null],
      ["license", "Licence Ouverte"],
    ];

    expect(toFiltersParams(value)).toEqual(params);
  });

  test("getFiltersValueFromParams", () => {
    const queryString = toQueryString(toFiltersParams(value));
    expect(queryString).toBe(
      "?geographical_coverage=France+m%C3%A9tropolitaine&format=file_gis&technical_source=Serveur+GIS&license=Licence+Ouverte"
    );
    expect(toFiltersValue(new URLSearchParams(queryString))).toEqual(value);
  });

  test("toFiltersOptions", () => {
    const options: DatasetFiltersOptions = {
      geographicalCoverage: [
        {
          label: "Métropole Européenne de Lille",
          value: "Métropole Européenne de Lille",
        },
        { label: "France métropolitaine", value: "France métropolitaine" },
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
      license: [
        { label: "Toutes les licences", value: "*" },
        { label: "Licence Ouverte", value: "Licence Ouverte" },
      ],
    };

    expect(toFiltersOptions(info)).toEqual(options);
  });
});
