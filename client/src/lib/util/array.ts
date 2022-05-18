export const range = (start: number, end: number): number[] => {
  const length = end - start;
  return Array.from({ length }, (_, idx) => start + idx);
};
