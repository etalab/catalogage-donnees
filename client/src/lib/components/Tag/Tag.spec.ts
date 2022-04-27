import "@testing-library/jest-dom";

import Tag from "./Tag.svelte";
import { render, fireEvent } from "@testing-library/svelte";

describe("Tag component", () => {
  test("A tag should have a name", async () => {
    const buttonText = "A nice text";
    const { getByText } = render(Tag, {
      id: 33,
      name: buttonText,
    });
    const button = getByText(buttonText);
    expect(button).toHaveTextContent(buttonText);
  });

  test("A tag should return its name and id after being clicked", async () => {
    const buttonText = "A nice text";
    const { getByText, component } = render(Tag, {
      id: 33,
      name: buttonText,
    });
    const button = getByText(buttonText);

    let tag: Tag;

    component.$on("click", (event) => {
      tag = event.detail;
    });
    await fireEvent.click(button);
    expect(tag).toEqual({ id: 33, name: buttonText });
  });
});
