/**
 * @jest-environment jsdom
 */

import "@testing-library/jest-dom";

import Home from "../routes/index.svelte";
import { fireEvent, render } from "@testing-library/svelte";

describe("Test the form", () => {
  test('The "Name" field is present', () => {
    const { getByLabelText } = render(Home);
    expect(getByLabelText("Name")).toBeInTheDocument();
  });
  test("The submit button is present", () => {
    const { getByRole } = render(Home);
    expect(getByRole("button")).toBeInTheDocument();
  });
  test("The submit button displays a loading text when clicked", async () => {
    const { getByRole } = render(Home);
    const submitButton = getByRole("button");

    expect(submitButton).toHaveTextContent("submit");

    await fireEvent.click(submitButton);
    expect(submitButton).toHaveTextContent("loading...");
  });
});
