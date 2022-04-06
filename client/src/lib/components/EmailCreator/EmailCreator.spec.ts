import "@testing-library/jest-dom";

import EmailCreator from "./EmailCreator.svelte";
import {
  render,
  fireEvent,
  getByRole as getByRoleIn,
} from "@testing-library/svelte";

describe("EmaiCreator component", () => {
  test("Contact emails can be added, filled and removed", async () => {
    const { getAllByTestId, getByRole } = render(EmailCreator, {
      props: {
        contactEmails: [],
      },
    });
    let inputs = getAllByTestId("contactEmail", { exact: false });
    expect(inputs.length).toBe(1);
    expect(inputs[0]).toHaveValue("");

    const addButton = getByRole("button", { name: /Ajouter/i });
    await fireEvent.click(addButton);
    inputs = getAllByTestId("contactEmail", { exact: false });
    expect(inputs.length).toBe(1);
    expect(inputs[0]).toHaveValue("");

    await fireEvent.input(inputs[0], {
      target: { value: "contact@example.org" },
    });
    inputs = getAllByTestId("contactEmail", { exact: false });

    expect(inputs[0]).toHaveValue("contact@example.org");

    const removeButton = getByRoleIn(inputs[0].parentElement, "button", {
      name: /Supprimer/i,
    });
    await fireEvent.click(removeButton);
    inputs = getAllByTestId("contactEmail", { exact: false });
    expect(inputs.length).toBe(1);
    expect(inputs[0]).toHaveValue("");
  });
});
