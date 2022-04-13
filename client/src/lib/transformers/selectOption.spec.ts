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
          value: "foo",
          label: "bar",
          id: "bar-0",
        },
        {
          value: "baz",
          label: "taz",
          id: "taz-1",
        },
      ]);
    });
  });
});
