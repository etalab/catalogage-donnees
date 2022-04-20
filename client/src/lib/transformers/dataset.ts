import _ from "lodash";
import type { Dataset } from "src/definitions/datasets";

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
  return transformKeysToUnderscoreCase(_.omit(data, "catalogRecord"));
};

export const toDataset = (item: any): Dataset => {
  const {
    catalog_record,
    entrypoint_email,
    contact_emails,
    update_frequency,
    last_updated_at,
    geographical_coverage,
    technical_source,
    ...rest
  } = item;
  const { created_at } = catalog_record;
  return {
    ...rest,
    catalogRecord: {
      createdAt: new Date(created_at),
    },
    entrypointEmail: entrypoint_email,
    contactEmails: contact_emails,
    updateFrequency: update_frequency,
    geographicalCoverage: geographical_coverage,
    technicalSource: technical_source,
    lastUpdatedAt: last_updated_at ? new Date(last_updated_at) : null,
  };
};
