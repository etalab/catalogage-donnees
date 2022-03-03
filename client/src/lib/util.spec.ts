import { toQueryString } from "./util";

describe("toQueryString", () => {
  const cases: [[string, string][], string][] = [
    [[], ""],
    [[["q", undefined]], ""],
    [[["q", null]], ""],
    [[["q", ""]], "?q="],
    [[["q", "value"]], "?q=value"],
    [[["a", "1"], ["b", "2"]], "?a=1&b=2"],
  ];

  test.each(cases)("When items is '%s'", (items, expected) => {
    expect(toQueryString(items)).toBe(expected);
  });
});
