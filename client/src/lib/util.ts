export const pluralize = (
  amount: number,
  singleText: string,
  pluralText: string
) => {
  if (amount === 1) {
    return singleText;
  }
  return pluralText;
};

/**
 * Create an URL query string, including a leading "?" if needed, dropping any null or undefined values.
 */
export const toQueryString = (items: [string, string | null | undefined][]) => {
  const definedItems = items.filter(([_, value]) => typeof value === "string");
  const params = new URLSearchParams();
  definedItems.forEach(([name, value]) => params.append(name, value));
  const qs = params.toString();
  return qs ? `?${qs}` : "";
};
