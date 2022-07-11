import {
  DATA_FORMAT_LABELS,
  GEOGRAPHICAL_COVERAGE_LABELS,
} from "src/constants";
import type { GeographicalCoverage } from "src/definitions/datasets";
import type {
  DatasetFiltersInfo,
  DatasetFiltersOptions,
  DatasetFiltersValue,
} from "src/definitions/datasetFilters";
import type { QueryParamRecord } from "src/definitions/url";
import { Maybe } from "../util/maybe";

export const toFiltersInfo = (data: any): DatasetFiltersInfo => {
  const { geographical_coverage, tag_id, technical_source, ...rest } = data;
  return {
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    tagId: tag_id,
    ...rest,
  };
};

export const toFiltersValue = (
  searchParams: URLSearchParams
): DatasetFiltersValue => {
  return {
    geographicalCoverage: searchParams.get(
      "geographical_coverage"
    ) as GeographicalCoverage | null,
    service: searchParams.get("service"),
    format: searchParams.get("format"),
    technicalSource: searchParams.get("technical_source"),
    tagId: searchParams.get("tag_id"),
  };
};

export const toFiltersParams = (
  value: DatasetFiltersValue
): QueryParamRecord => {
  const { geographicalCoverage, service, format, technicalSource, tagId } =
    value;

  return [
    ["geographical_coverage", geographicalCoverage],
    ["service", service],
    ["format", format],
    ["technical_source", technicalSource],
    ["tag_id", tagId],
  ];
};

export const toFiltersOptions = (
  info: DatasetFiltersInfo
): DatasetFiltersOptions => {
  return {
    geographicalCoverage: info.geographicalCoverage.map((value) => ({
      label: GEOGRAPHICAL_COVERAGE_LABELS[value],
      value,
    })),
    service: info.service.map((value) => ({ label: value, value })),
    format: info.format.map((value) => ({
      label: DATA_FORMAT_LABELS[value],
      value,
    })),
    technicalSource: info.technicalSource.map((value) => ({
      label: value,
      value,
    })),
    tagId: info.tagId.map((tag) => ({ label: tag.name, value: tag.id })),
  };
};

export const toFiltersButtonTexts = (
  value: DatasetFiltersValue,
  tagIdToName: Record<string, string>
): { [K in keyof DatasetFiltersValue]: Maybe<string> } => {
  return {
    geographicalCoverage: Maybe.map(
      value.geographicalCoverage,
      (v) => GEOGRAPHICAL_COVERAGE_LABELS[v]
    ),
    service: value.service,
    format: Maybe.map(value.format, (v) => DATA_FORMAT_LABELS[v]),
    technicalSource: value.technicalSource,
    tagId: Maybe.map(value.tagId, (v) => tagIdToName[v]),
  };
};