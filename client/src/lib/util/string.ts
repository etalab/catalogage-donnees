export const escape = (value: string): string => {
  // See: https://stackoverflow.com/a/3561711
  return value.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
};
