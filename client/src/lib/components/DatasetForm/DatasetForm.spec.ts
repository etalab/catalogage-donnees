import "@testing-library/jest-dom";

import DatasetForm from "./DatasetForm.svelte";
import { render, fireEvent } from "@testing-library/svelte";
import type { DataFormat } from "src/definitions/datasets";
import { UPDATE_FREQUENCY } from "src/constants";
import { getFakeDataSetFormData } from "src/fixtures/dataset";

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

  test('The "contact email" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const inputs = getByLabelText("E-mail de contact", { exact: false });

    expect(inputs).toBeRequired();
    expect(inputs).toHaveAttribute("type", "email");
  });

  test('The "service field" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const service = getByLabelText("Service producteur de la donnée", {
      exact: false,
    });
    expect(service).toBeInTheDocument();
    expect(service).toBeRequired();
    expect(service).toHaveAttribute("type", "text");
  });

  test('The "last published at" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const service = getByLabelText("Date de la dernière mise à jour", {
      exact: false,
    });
    expect(service).toBeInTheDocument();
    expect(service).toBeRequired();
    expect(service).toHaveAttribute("type", "date");
  });

  test('The "updateFrequency" field is present', () => {
    const { getByLabelText } = render(DatasetForm);
    const updateFrequency = getByLabelText("Fréquence de mise à jour", {
      exact: false,
    });
    expect(updateFrequency).toBeInTheDocument();
    expect(updateFrequency).toBeRequired();
    expect(updateFrequency.children.length).toBe(7);
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
    const initial = getFakeDataSetFormData({
      title: "Titre initial",
      description: "Description initiale",
      formats: ["website"],
      entrypointEmail: "service.initial@example.org",
      contactEmail: "person@example.org",
      firstPublishedAt: new Date().toISOString(),
      updateFrequency: UPDATE_FREQUENCY.daily,
      service: "Drac",
    });
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

    const entrypointEmail = getByLabelText("Adresse e-mail fonctionnelle", {
      exact: false,
    }) as HTMLInputElement;
    expect(entrypointEmail.value).toBe("service.initial@example.org");

    const inputs = getByLabelText("E-mail de contact", {
      exact: false,
    }) as HTMLInputElement;

    expect(inputs.value).toBe("person@example.org");
  });
});
