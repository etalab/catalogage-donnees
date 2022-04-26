import type { Fetch } from "src/definitions/fetch";
import type { Tag } from "src/definitions/tag";
import { getApiUrl, getHeaders } from "../fetch";

type GetTags = (opts: { fetch: Fetch; apiToken: string }) => Promise<Tag[]>;

export const getTags: GetTags = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/tags`;
  const request = new Request(url, {
    headers: getHeaders(apiToken),
  });
  const response = await fetch(request);
  return response.json();
};
