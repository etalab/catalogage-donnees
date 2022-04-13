import { toSelectOption } from "./selectOption";

describe("transformers -- selectOption", () => {
  describe("toSelectOption", () => {
    it("should transform an object to SelectOption", () => {
      const source = {
        foo: "bar",
        baz: "taz",
      };

      expect(toSelectOption(source)).toEqual([
        {
          value: "bar",
          label: "foo",
          id: "bar-0",
        },
        {
          value: "taz",
          label: "baz",
          id: "taz-1",
        },
      ]);
    });
  });
});
