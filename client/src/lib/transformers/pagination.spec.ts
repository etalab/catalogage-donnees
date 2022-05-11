import { toPaginated } from "./pagination";

describe("transformers -- pagination", () => {
  const data = {
    items: [1, 2, 3],
    total_items: 3,
    total_pages: 4,
  };

  test("the data is transformed", () => {
    const transformed = toPaginated(data);
    expect(transformed).toStrictEqual({
      items: [1, 2, 3],
      totalItems: 3,
      totalPages: 4,
    });
  });

  test("items are mapped", () => {
    const transformed = toPaginated(data, (item) => `${item * 2} items`);
    expect(transformed.items).toStrictEqual(["2 items", "4 items", "6 items"]);
  });
});
