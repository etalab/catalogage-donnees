import { Maybe } from "./maybe";

/**
 * Create an URL query string, including a leading "?" if needed, dropping any null or undefined values.
 */
export const toQueryString = (items: [string, Maybe<string>][]): string => {
  const params = new URLSearchParams();
  items.forEach(([name, value]) => {
    if (Maybe.Some(value)) {
      params.append(name, value);
    }
  });
  const qs = params.toString();
  return qs ? `?${qs}` : "";
};
