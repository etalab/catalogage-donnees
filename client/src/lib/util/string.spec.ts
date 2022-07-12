import { escape } from "./string";

test("escape", () => {
  expect(escape("test")).toBe("test");
  expect(escape("Autre (ouverte)")).toBe("Autre \\(ouverte\\)");
  const s = "Autre (ouverte) test";
  expect(s.match(new RegExp(escape("Autre (ouverte)"), "i"))).toBeTruthy();
});
