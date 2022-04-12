import format from "date-fns/format";
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
  const transformed = transformKeysToUnderscoreCase(data);
  return {
    ...transformed,
    last_updated_at: new Date(data.lastUpdatedAt).toISOString(),
  };
};

export const toDataset = (item: any): Dataset => {
  const {
    created_at,
    entrypoint_email,
    contact_emails,
    update_frequency,
    last_updated_at,
    ...rest
  } = item;
  return {
    ...rest,
    createdAt: new Date(created_at),
    entrypointEmail: entrypoint_email,
    contactEmails: contact_emails,
    updateFrequency: update_frequency,
    lastUpdatedAt: format(new Date(last_updated_at), "yyyy-MM-dd"),
  };
};
