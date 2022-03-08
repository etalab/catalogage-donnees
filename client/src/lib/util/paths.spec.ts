import { path } from "./paths";

test("path", () => {
  expect(path("/")({})).toBe("/");
  expect(path("/login")({})).toBe("/login");
  expect(path("/:itemId")({ itemId: "abc" })).toBe("/abc");
  expect(path("/items/:itemId")({ itemId: "abc" })).toBe("/items/abc");
  expect(
    path("/items/:itemId/objects/:objectId/")({
      itemId: "abc",
      objectId: "123",
    })
  ).toBe("/items/abc/objects/123/");
  expect(() => path("/items/:itemId")({} as any)).toThrow();
});
