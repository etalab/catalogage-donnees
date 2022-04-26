import { toSelectOptions } from "./form";

import type { Tag } from "src/definitions/tag";
import { transformTagToSelectOption } from "./form";

describe("transformers -- form", () => {
  test("should transform an object to SelectOption", () => {
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

  test("should transform tag to select option", () => {
    const tag: Tag = {
      id: 3,
      name: "foo",
    };
    expect(transformTagToSelectOption(tag)).toEqual({
      label: "foo",
      value: "3",
    });
  });
});
