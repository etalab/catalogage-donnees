import type { Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders, makeApiRequest } from "../fetch";
import { Maybe } from "../util/maybe";

type GetLicenses = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<Maybe<string[]>>;

export const getLicenses: GetLicenses = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/licenses/`;
  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });
  const response = await makeApiRequest(fetch, request);
  return Maybe.map(response, (response) => response.json());
};
