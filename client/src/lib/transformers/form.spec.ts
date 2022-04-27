import { toSelectOptions } from "./form";
import { transformTagToSelectOption } from "./form";
import { buildFakeTag } from "src/tests/factories/tags";

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
    const tag = buildFakeTag();
    expect(transformTagToSelectOption(tag)).toEqual({
      label: tag.name,
      value: tag.id,
    });
  });
});
