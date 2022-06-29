import type { QueryParamRecord } from "src/definitions/url";
import { Maybe } from "./maybe";

/**
 * Create an URL query string, including a leading "?" if needed, dropping any null or undefined values.
 */
export const toQueryString = (items: QueryParamRecord): string => {
  return patchQueryString(new URLSearchParams(), items);
};

export const patchQueryString = (
  params: URLSearchParams,
  items: [string, Maybe<string>][]
): string => {
  const newParams = new URLSearchParams(params);
  items.forEach(([name, value]) => {
    if (Maybe.Some(value)) {
      newParams.set(name, value);
    }
  });
  const qs = newParams.toString();
  return qs ? `?${qs}` : "";
};
