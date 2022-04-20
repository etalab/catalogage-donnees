import "@testing-library/jest-dom";

import Tag from "./Tag.svelte";
import {
  render,
  fireEvent,
  getByRole as getByRoleIn,
} from "@testing-library/svelte";

describe("Tag component", () => {
  test("A tag  should have a name ", async () => {
    const buttonText = "A nice text";
    const { getByText } = render(Tag, {
      name: buttonText,
    });
    const button = getByText(buttonText);
    expect(button).toHaveTextContent(buttonText);
  });

  test.only("A tag should return his label after being clicked", async () => {
    const buttonText = "A nice text";
    const { getByText, component } = render(Tag, {
      name: buttonText,
    });
    const button = getByText(buttonText);

    component.$on("select", (event) => {
      expect(event.detail).toBe(buttonText);
    });
    await fireEvent.click(button);
  });
});
