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
 * Create an URL query string, dropping any null or undefined values.
 */
export const toQueryString = (items: [string, string | null | undefined][]) => {
  const definedItems = items.filter(([_, value]) => typeof value === "string");
  const params = new URLSearchParams();
  definedItems.forEach(([name, value]) => params.append(name, value));
  return params.toString();
};
