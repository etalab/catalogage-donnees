import type { DatasetFiltersInfo } from "src/definitions/datasetFilters";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders, makeApiRequest } from "../fetch";
import { toFiltersInfo } from "../transformers/datasetFilters";
import { Maybe } from "../util/maybe";

type GetDatasetFiltersInfo = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<Maybe<DatasetFiltersInfo>>;

export const getDatasetFiltersInfo: GetDatasetFiltersInfo = async ({
  fetch,
  apiToken,
}) => {
  const url = `${getApiUrl()}/datasets/filters/`;

  const request = new Request(url, {
    headers: new Headers(getHeaders(apiToken)),
  });

  const response = await makeApiRequest(fetch, request);

  return Maybe.map(response, async (response) => {
    const data = await response.json();
    return toFiltersInfo(data);
  });
};
