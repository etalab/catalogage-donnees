import { pluralize } from "./format";

test("pluralize", () => {
  expect(`0 résultat${pluralize(0, "", "s")}`).toBe("0 résultats");
  expect(`1 ${pluralize(1, "cheval", "chevaux")}`).toBe("1 cheval");
  expect(`2 jour${pluralize(2, "", "s")}`).toBe("2 jours");
  expect(`3 ${pluralize(3, "cheval", "chevaux")}`).toBe("3 chevaux");
});
