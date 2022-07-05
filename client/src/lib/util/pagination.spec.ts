import { getPageFromParams, makePageParam } from "./pagination";

describe("pagination", () => {
  test("makePageParam", () => {
    expect(makePageParam(1)).toEqual(["page", "1"]);
  });

  test("getPageFromParams", () => {
    expect(getPageFromParams(new URLSearchParams())).toBe(1);
    expect(getPageFromParams(new URLSearchParams("page=3"))).toBe(3);
  });
});
