import {
  DATA_FORMAT_LABELS,
  GEOGRAPHICAL_COVERAGE_LABELS,
} from "src/constants";
import type {
  Dataset,
  DatasetFilters,
  SelectableDatasetFilter,
} from "src/definitions/datasets";
import type { SelectOption } from "src/definitions/form";
import type { Tag } from "src/definitions/tag";
import { omit } from "../util/object";

export const camelToUnderscore = (key: string): string => {
  return key.replace(/([A-Z])/g, "_$1").toLowerCase();
};

export const transformKeysToUnderscoreCase = (object: {
  [K: string]: unknown;
}): { [K: string]: unknown } => {
  return Object.keys(object).reduce((previous, current) => {
    return {
      ...previous,
      [camelToUnderscore(current)]: object[current],
    };
  }, {});
};

export const toPayload = (
  data: Partial<Record<keyof Dataset, any>>
): { [K: string]: unknown } => {
  const payload = transformKeysToUnderscoreCase(omit(data, ["catalogRecord"]));
  payload.license = null;
  return payload;
};

export const toDataset = (item: any): Dataset => {
  const {
    catalog_record,
    producer_email,
    contact_emails,
    update_frequency,
    last_updated_at,
    geographical_coverage,
    technical_source,
    url,
    ...rest
  } = item;
  const { created_at } = catalog_record;
  return {
    ...rest,
    catalogRecord: {
      createdAt: new Date(created_at),
    },
    producerEmail: producer_email,
    contactEmails: contact_emails,
    updateFrequency: update_frequency,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    lastUpdatedAt: last_updated_at ? new Date(last_updated_at) : null,
    url,
  };
};

const mapToOption = (items: string[]): SelectOption[] =>
  items.map((item) => {
    return {
      label: item,
      value: item,
    };
  });

const mapTagToSelectOption = (items: Tag[]): SelectOption[] =>
  items.map((item) => {
    return {
      label: item.name,
      value: item.id,
    };
  });

const mapGeographicalCoverageToSelectOption = (
  items: string[]
): SelectOption[] =>
  items.map((item) => {
    return {
      label: GEOGRAPHICAL_COVERAGE_LABELS[item],
      value: item,
    };
  });

const mapDataFormatToSelectOption = (items: string[]): SelectOption[] =>
  items.map((item) => {
    return {
      label: DATA_FORMAT_LABELS[item],
      value: item,
    };
  });

export const transformSearchFiltersIntoSelectableDatasetFilters = (
  source: DatasetFilters
): SelectableDatasetFilter => {
  return {
    format: source.format ? mapDataFormatToSelectOption(source.format) : null,
    geographical_coverage: source.geographical_coverage
      ? mapGeographicalCoverageToSelectOption(source.geographical_coverage)
      : null,
    service: source.service ? mapToOption(source.service) : null,
    tag_id: source.tag_id ? mapTagToSelectOption(source.tag_id) : null,
    technical_source: source.technical_source
      ? mapToOption(source.technical_source)
      : null,
  };
};
