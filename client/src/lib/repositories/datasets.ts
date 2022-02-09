import type { Dataset } from "src/definitions/datasets";
import type { Fetch } from "src/definitions/fetch";
import { getApiUrl } from "$lib/fetch";

type GetDatasets = (opts: { fetch: Fetch }) => Promise<Dataset[]>;

export const getDatasets: GetDatasets = async ({ fetch }) => {
  const url = `${getApiUrl()}/datasets/`;
  const request = new Request(url);
  const response = await fetch(request);
  return await response.json();
};
