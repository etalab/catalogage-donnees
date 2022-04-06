
import "@testing-library/jest-dom";

import DatasetForm from "./DatasetForm.svelte";
import {
    render,
    fireEvent,
    getByRole as getByRoleIn,
} from "@testing-library/svelte";


describe.skip("EmaiCreator component", () => {
    test("Contact emails can be added, filled and removed", async () => {
        const { getAllByLabelText, getByRole } = render(DatasetForm);
        let inputs = getAllByLabelText(/Contact \d/);
        expect(inputs.length).toBe(1);
        expect(inputs[0]).toHaveValue("");

        const addButton = getByRole("button", { name: /Ajouter/i });
        await fireEvent.click(addButton);
        inputs = getAllByLabelText(/Contact \d/);
        expect(inputs.length).toBe(2);
        expect(inputs[0]).toHaveValue("");
        expect(inputs[1]).toHaveValue("");

        await fireEvent.input(inputs[1], {
            target: { value: "contact@example.org" },
        });
        inputs = getAllByLabelText(/Contact \d/);
        expect(inputs[0]).toHaveValue("");
        expect(inputs[1]).toHaveValue("contact@example.org");

        const removeButton = getByRoleIn(inputs[1].parentElement, "button", {
            name: /Supprimer/i,
        });
        await fireEvent.click(removeButton);
        inputs = getAllByLabelText(/Contact \d/);
        expect(inputs.length).toBe(1);
        expect(inputs[0]).toHaveValue("");
    });
})

