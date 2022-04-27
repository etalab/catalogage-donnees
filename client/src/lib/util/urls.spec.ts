import { toQueryString } from "./urls";

describe("toQueryString", () => {
  const cases: [[string, string | null | undefined][], string][] = [
    [[], ""],
    [[["q", undefined]], ""],
    [[["q", null]], ""],
    [[["q", ""]], "?q="],
    [[["q", "value"]], "?q=value"],
    [
      [
        ["q", "value"],
        ["limit", "100"],
        ["sort", "+date"],
      ],
      "?q=value&limit=100&sort=%2Bdate",
    ],
  ];

  test.each(cases)("When items is '%s'", (items, expected) => {
    expect(toQueryString(items)).toBe(expected);
  });
});
