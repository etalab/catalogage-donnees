import "@testing-library/jest-dom";

import DatasetForm from "./DatasetForm.svelte";
import { render } from "@testing-library/svelte";
import type { DataFormat, DatasetFormData } from "src/definitions/datasets";

describe("Test the dataset form", () => {
  test('The "title" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    expect(getByLabelText("Nom", { exact: false })).toBeInTheDocument();
  });
  test('The "description" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    expect(getByLabelText("Description", { exact: false })).toBeInTheDocument();
  });
  test('The "formats" field is present', () => {
    const { getByText } = render(DatasetForm);
    expect(
      getByText("Format(s) des données", { exact: false })
    ).toBeInTheDocument();
  });
  test("The submit button is present", () => {
    const { getByRole } = render(DatasetForm);
    expect(getByRole("button")).toBeInTheDocument();
  });
  test("The submit button displays a loading text when loading", async () => {
    const props = { submitLabel: "Envoyer", loadingLabel: "Ça charge..." };

    const { getByRole, rerender } = render(DatasetForm, { props });
    let submitButton = getByRole("button");
    expect(submitButton).toHaveTextContent("Envoyer");

    rerender({ props: { ...props, loading: true } });
    submitButton = getByRole("button");
    expect(submitButton).toHaveTextContent("Ça charge...");
  });
  test("The fields are initialized with initial values", async () => {
    const initial: DatasetFormData = {
      title: "Titre initial",
      description: "Description initiale",
      formats: ["website"],
    };
    const props = { initial };

    const { getByLabelText, container } = render(DatasetForm, { props });

    const title = getByLabelText("Nom", { exact: false }) as HTMLInputElement;
    expect(title.value).toBe("Titre initial");

    const description = getByLabelText("Description", {
      exact: false,
    }) as HTMLInputElement;
    expect(description.value).toBe("Description initiale");

    const getFormatCheckbox = (value: DataFormat) =>
      container.querySelector(`input[value='${value}']`);
    expect(getFormatCheckbox("file_tabular")).not.toBeChecked();
    expect(getFormatCheckbox("file_gis")).not.toBeChecked();
    expect(getFormatCheckbox("api")).not.toBeChecked();
    expect(getFormatCheckbox("database")).not.toBeChecked();
    expect(getFormatCheckbox("website")).toBeChecked();
    expect(getFormatCheckbox("other")).not.toBeChecked();
  });
});
