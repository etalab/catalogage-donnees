/**
 * @jest-environment jsdom
 */

import "@testing-library/jest-dom";

import Contribuer from "../routes/contribuer/index.svelte";
import { fireEvent, render } from "@testing-library/svelte";

describe("Test the contribution form", () => {
  test('The "title" field is present', () => {
    const { getByLabelText } = render(Contribuer);
    expect(getByLabelText("Nom", { exact: false })).toBeInTheDocument();
  });
  test('The "description" field is present', () => {
    const { getByLabelText } = render(Contribuer);
    expect(getByLabelText("Description", { exact: false })).toBeInTheDocument();
  });
  test("The submit button is present", () => {
    const { getByRole } = render(Contribuer);
    expect(getByRole("button")).toBeInTheDocument();
  });
  test("The submit button displays a loading text when clicked", async () => {
    const { getByRole } = render(Contribuer);
    const submitButton = getByRole("button");

    expect(submitButton).toHaveTextContent("Contribuer");

    await fireEvent.click(submitButton);
    expect(submitButton).toHaveTextContent("Contribution");
  });
});
