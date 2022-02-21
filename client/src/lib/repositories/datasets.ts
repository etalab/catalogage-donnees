import type { Dataset, DatasetCreateData } from "src/definitions/datasets";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl } from "$lib/fetch";

type GetDatasetByID = (opts: { fetch: Fetch, id: string }) => Promise<Dataset>;

export const getDatasetByID: GetDatasetByID = async ({ fetch, id }) => {
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url);
  const response = await fetch(request);
  return await response.json();
}

type GetDatasets = (opts: { fetch: Fetch }) => Promise<Dataset[]>;

export const getDatasets: GetDatasets = async ({ fetch }) => {
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url);
  const response = await fetch(request);
  return await response.json();
};

type CreateDataset = (opts: {
  fetch: Fetch;
  data: DatasetCreateData;
}) => Promise<Dataset>;

export const createDataset: CreateDataset = async ({ fetch, data }) => {
  const body = JSON.stringify(data);
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });
  const response = await fetch(request);
  return await response.json();
};
