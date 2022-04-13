import "@testing-library/jest-dom";

import DatasetForm from "./DatasetForm.svelte";
import { render, fireEvent, waitFor } from "@testing-library/svelte";
import type { DataFormat, DatasetFormData } from "src/definitions/datasets";
import { GEOGRAPHICAL_COVERAGE_LABELS } from "src/constants";

describe("Test the dataset form", () => {
  test('The "title" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const title = getByLabelText("Nom", { exact: false });
    expect(title).toBeInTheDocument();
    expect(title).toBeRequired();
  });

  test('The "description" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const description = getByLabelText("Description", { exact: false });
    expect(description).toBeInTheDocument();
    expect(description).toBeRequired();
  });

  test('The "formats" field is present', async () => {
    const { getAllByRole } = render(DatasetForm);
    const checkboxes = getAllByRole("checkbox");
    expect(checkboxes.length).toBeGreaterThan(0);
  });

  test('The "geographicalCoverage" field is present', async () => {
    const { getByLabelText } = render(DatasetForm);
    const geographicalCoverage = getByLabelText("Couverture géographique", {
      exact: false,
    });
    expect(geographicalCoverage).toBeInTheDocument();
    expect(geographicalCoverage).toBeRequired();
  });

  test("At least one format is required", async () => {
    const { getAllByRole } = render(DatasetForm);
    const checkboxes = getAllByRole("checkbox", { checked: false });
    checkboxes.forEach((checkbox) => expect(checkbox).toBeRequired());
    await fireEvent.click(checkboxes[0]);
    expect(checkboxes[0]).toBeChecked();
    checkboxes
      .slice(1)
      .forEach((checkbox) => expect(checkbox).not.toBeChecked());
    checkboxes.forEach((checkbox) => expect(checkbox).not.toBeRequired());
  });

  test('The "entrypoint email" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const entrypointEmail = getByLabelText("Adresse e-mail fonctionnelle", {
      exact: false,
    });
    expect(entrypointEmail).toBeInTheDocument();
    expect(entrypointEmail).toBeRequired();
    expect(entrypointEmail).toHaveAttribute("type", "email");
  });

  test('The "contact emails" field is present', () => {
    const { getAllByLabelText } = render(DatasetForm);
    const inputs = getAllByLabelText(/Contact \d/);
    expect(inputs.length).toBe(1);
    expect(inputs[0]).not.toBeRequired();
    expect(inputs[0]).toHaveAttribute("type", "email");
  });

  test("The submit button is present", () => {
    const { getByRole } = render(DatasetForm);
    expect(getByRole("button", { name: /Publier/i })).toBeInTheDocument();
  });

  test("The submit button displays a loading text when loading", async () => {
    const props = { submitLabel: "Envoyer", loadingLabel: "Ça charge..." };

    const { getByRole, rerender } = render(DatasetForm, { props });
    expect(getByRole("button", { name: "Envoyer" })).toBeInTheDocument();

    rerender({ props: { ...props, loading: true } });
    expect(getByRole("button", { name: /Ça charge/i })).toBeInTheDocument();
  });

  test("The fields are initialized with initial values", async () => {
    const initial: DatasetFormData = {
      title: "Titre initial",
      description: "Description initiale",
      formats: ["website"],
      entrypointEmail: "service.initial@example.org",
      contactEmails: ["person@example.org"],
      service: "A nice service",
      lastUpdatedAt: new Date("2022-02-01"),
      updateFrequency: "never",
      geographicalCoverage: "europe",
    };
    const props = { initial };

    const { getByLabelText, getAllByLabelText, container } = render(
      DatasetForm,
      { props }
    );

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

    const entrypointEmail = getByLabelText("Adresse e-mail fonctionnelle", {
      exact: false,
    }) as HTMLInputElement;
    expect(entrypointEmail.value).toBe("service.initial@example.org");

    const contactEmails = getAllByLabelText(/Contact \d/);
    expect(contactEmails.length).toBe(1);
    expect(contactEmails[0]).toHaveValue("person@example.org");

    const lastUpdatedAt = getByLabelText("Date de la dernière mise à jour", {
      exact: false,
    }) as HTMLInputElement;
    expect(lastUpdatedAt.value).toBe("2022-02-01");

    const updateFrequency = getByLabelText("Fréquence de mise à jour", {
      exact: false,
    }) as HTMLSelectElement;
    expect(updateFrequency.value).toBe("never");
  });

  test("Null fields are correctly handled in HTML and submitted as null", async () => {
    const initial: DatasetFormData = {
      title: "Titre initial",
      description: "Description initiale",
      formats: ["website"],
      entrypointEmail: "service.initial@example.org",
      contactEmails: ["person@example.org"],
      service: "A nice service",
      lastUpdatedAt: null,
      updateFrequency: null,
      geographicalCoverage: "europe",
    };
    const props = { initial };
    const { getByLabelText, getByRole, component } = render(DatasetForm, {
      props,
    });

    const lastUpdatedAt = getByLabelText("Date de la dernière mise à jour", {
      exact: false,
    }) as HTMLInputElement;
    expect(lastUpdatedAt.value).toBe("");

    const updateFrequency = getByLabelText("Fréquence de mise à jour", {
      exact: false,
    }) as HTMLSelectElement;
    expect(updateFrequency.value).toBe("null");

    // Simulate touching the fields. This sends HTML values such as "" (empty date or select value)
    // which should be handled as null.
    await fireEvent.blur(lastUpdatedAt);
    await fireEvent.blur(updateFrequency);

    let submittedValue: DatasetFormData;
    component.$on("save", (event) => (submittedValue = event.detail));
    const form = getByRole("form");
    await fireEvent.submit(form);
    await waitFor(() => expect(submittedValue).toBeDefined());
    expect(submittedValue.lastUpdatedAt).toBe(null);
    expect(submittedValue.updateFrequency).toBe(null);
  });
});
