import type { Fetch } from "src/definitions/fetch";
import type { Tag } from "src/definitions/tag";
import { getApiUrl, getHeaders, makeApiRequest } from "../fetch";
import { Maybe } from "../util/maybe";

type GetTags = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<Maybe<Tag[]>>;
export const getTags: GetTags = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/tags/`;
  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });
  const response = await makeApiRequest(fetch, request);
  return Maybe.map(response, (response) => response.json());
};
