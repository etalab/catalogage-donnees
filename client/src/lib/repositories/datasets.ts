import type {
  Dataset,
  DatasetCreateData,
  DatasetUpdateData,
} from "src/definitions/datasets";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl } from "$lib/fetch";
import { toQueryString } from "$lib/util/urls";

const toDataset = (item: any): Dataset => {
  const { created_at, entrypoint_email, contact_emails, ...rest } = item;
  return {
    ...rest,
    createdAt: new Date(created_at),
    entrypointEmail: entrypoint_email,
    contactEmails: contact_emails,
  };
};

const toPayload = (data: Partial<Record<keyof Dataset, any>>) => {
  const { entrypointEmail, contactEmails, ...rest } = data;
  return {
    ...rest,
    entrypoint_email: entrypointEmail,
    contact_emails: contactEmails,
    // Expected by API, update when frontend app is ready
    service: "DUMMY",
    update_frequency: null,
    last_updated_at: null,
  };
};

type GetDatasetByID = (opts: { fetch: Fetch; id: string }) => Promise<Dataset>;

export const getDatasetByID: GetDatasetByID = async ({ fetch, id }) => {
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url);
  const response = await fetch(request);
  return toDataset(await response.json());
};

type GetDatasets = (opts: { fetch: Fetch; q?: string }) => Promise<Dataset[]>;

export const getDatasets: GetDatasets = async ({ fetch, q }) => {
  const queryItems = [];
  if (typeof q === "string") {
    queryItems.push(["q", q], ["highlight", "true"]);
  }
  const queryString = toQueryString(queryItems);
  const url = `${getApiUrl()}/datasets/${queryString}`;
  const request = new Request(url);
  const response = await fetch(request);
  const items: any[] = await response.json();
  return items.map((item) => toDataset(item));
};

type CreateDataset = (opts: {
  fetch: Fetch;
  data: DatasetCreateData;
}) => Promise<Dataset>;

export const createDataset: CreateDataset = async ({ fetch, data }) => {
  const body = JSON.stringify(toPayload(data));
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });
  const response = await fetch(request);
  return toDataset(await response.json());
};

type UpdateDataset = (opts: {
  fetch: Fetch;
  id: string;
  data: DatasetUpdateData;
}) => Promise<Dataset>;

export const updateDataset: UpdateDataset = async ({ fetch, id, data }) => {
  const body = JSON.stringify(toPayload(data));
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body,
  });
  const response = await fetch(request);
  return toDataset(await response.json());
};
