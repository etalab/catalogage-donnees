import { range } from "./array";

describe("range", () => {
  const cases: [number, number, number[]][] = [
    [1, 1, []],
    [2, 1, []],
    [2, 2, []],
    [1, 2, [1]],
    [1, 3, [1, 2]],
    [2, 5, [2, 3, 4]],
    [-3, 2, [-3, -2, -1, 0, 1]],
  ];

  test.each(cases)("when start=%s and end=%s", (start, end, expected) => {
    expect(range(start, end)).toStrictEqual(expected);
  });
});
