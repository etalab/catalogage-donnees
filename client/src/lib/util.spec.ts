import { toQueryString } from "./util";

describe("toQueryString", () => {
  const cases: [[string, string][], string][] = [
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
