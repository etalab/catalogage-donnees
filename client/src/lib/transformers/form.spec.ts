import { toSelectOptions } from "./form";

describe("transformers -- form", () => {
  describe("toSelectOptions", () => {
    it("should transform an object to SelectOption", () => {
      const source = {
        foo: "bar",
        baz: "taz",
      };

      expect(toSelectOptions(source)).toEqual([
        {
          value: "foo",
          label: "bar",
        },
        {
          value: "baz",
          label: "taz",
        },
      ]);
    });
  });
});
