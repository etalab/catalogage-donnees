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
