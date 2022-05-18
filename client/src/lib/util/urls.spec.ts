import type { Maybe } from "./maybe";
import { patchQueryString, toQueryString } from "./urls";

describe("toQueryString", () => {
  const cases: [[string, Maybe<string>][], string][] = [
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

describe("patchQueryString", () => {
  const cases: [URLSearchParams, [string, Maybe<string>][], string][] = [
    [new URLSearchParams(), [], ""],
    [new URLSearchParams("a=1"), [], "?a=1"],
    [new URLSearchParams("a=1"), [["a", "1"]], "?a=1"],
    [
      new URLSearchParams("a=1"),
      [
        ["b", "2"],
        ["c", null],
        ["d", ""],
        ["e", "3"],
      ],
      "?a=1&b=2&d=&e=3",
    ],
  ];

  test.each(cases)(
    "When initial is '%s' and items is '%s'",
    (initial, items, expected) => {
      expect(patchQueryString(initial, items)).toBe(expected);
    }
  );
});
