import type {
  Dataset,
  DatasetCreateData,
  DatasetUpdateData,
} from "src/definitions/datasets";
import type { Fetch } from "src/definitions/fetch";
import type { Paginated } from "src/definitions/pagination";
import { DATASETS_PER_PAGE } from "src/constants";
import { getHeaders, getApiUrl, makeApiRequest } from "$lib/fetch";
import { toQueryString } from "$lib/util/urls";
import { toDataset, toPayload } from "$lib/transformers/dataset";
import { toPaginated } from "$lib/transformers/pagination";
import { Maybe } from "$lib/util/maybe";
import type { SearchFilter } from "src/definitions/searchFilters";

type GetDatasetByID = (opts: {
  fetch: Fetch;
  apiToken: string;
  id: string;
}) => Promise<Maybe<Dataset>>;

export const getDatasetByID: GetDatasetByID = async ({
  fetch,
  apiToken,
  id,
}) => {
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) =>
    toDataset(await response.json())
  );
};

type GetDatasets = (opts: {
  fetch: Fetch;
  apiToken: string;
  page: number;
  q?: string;
}) => Promise<Maybe<Paginated<Dataset>>>;

export const getDatasets: GetDatasets = async ({
  fetch,
  apiToken,
  page,
  q,
}) => {
  const queryItems: [string, string][] = [
    ["page_number", page.toString()],
    ["page_size", DATASETS_PER_PAGE.toString()],
  ];

  if (typeof q === "string") {
    queryItems.push(["q", q]);
  }

  const queryString = toQueryString(queryItems);
  const url = `${getApiUrl()}/datasets/${queryString}`;

  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) => {
    const data = await response.json();
    return toPaginated(data, (item) => toDataset(item));
  });
};

type CreateDataset = (opts: {
  fetch: Fetch;
  apiToken: string;
  data: DatasetCreateData;
}) => Promise<Maybe<Dataset>>;

export const createDataset: CreateDataset = async ({
  fetch,
  apiToken,
  data,
}) => {
  const body = JSON.stringify(toPayload(data));
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url, {
    method: "POST",
    headers: new Headers([
      ["Content-Type", "application/json"],
      ...getHeaders(apiToken),
    ]),
    body,
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) =>
    toDataset(await response.json())
  );
};

type UpdateDataset = (opts: {
  fetch: Fetch;
  apiToken: string;
  id: string;
  data: DatasetUpdateData;
}) => Promise<Maybe<Dataset>>;

export const updateDataset: UpdateDataset = async ({
  fetch,
  apiToken,
  id,
  data,
}) => {
  const body = JSON.stringify(toPayload(data));
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    method: "PUT",
    headers: new Headers([
      ["Content-Type", "application/json"],
      ...getHeaders(apiToken),
    ]),
    body,
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) =>
    toDataset(await response.json())
  );
};

type DeleteDataset = (opts: {
  fetch: Fetch;
  apiToken: string;
  id: string;
}) => Promise<void>;

export const deleteDataset: DeleteDataset = async ({ fetch, apiToken, id }) => {
  const url = `${getApiUrl()}/datasets/${id}/`;
  const request = new Request(url, {
    method: "DELETE",
    headers: new Headers(getHeaders(apiToken)),
  });
  await makeApiRequest(fetch, request);
};


export const getSearchFilter = async (fetch: Fetch, apiToken: string): Promise<Maybe<SearchFilter>> => {
  const url = `${getApiUrl()}/datasets/filters/`;
  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  const response = (await makeApiRequest(fetch, request))

  return Maybe.map(response, (response) => response.json());
};
