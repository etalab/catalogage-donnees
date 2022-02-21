import "@testing-library/jest-dom";

import DatasetForm from "./DatasetForm.svelte";
import { render } from "@testing-library/svelte";

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
});
