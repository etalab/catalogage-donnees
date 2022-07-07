/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import { render, fireEvent } from "@testing-library/svelte";
import LicenseField from "./_LicenseField.svelte";

describe("License field", () => {
  test("should have an input", () => {
    const { getByRole } = render(LicenseField);
    const input = getByRole("combobox");
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute("autocomplete", "off");
  });

  test("should show nothing on click if no suggestions", async () => {
    const { getByRole, queryAllByRole } = render(LicenseField);
    await fireEvent.focus(getByRole("combobox"));
    const options = queryAllByRole("option");
    expect(options.length).toBe(0);
  });

  test("should show suggestions on click", async () => {
    const { getByRole, getAllByRole } = render(LicenseField, {
      props: { suggestions: ["Licence Ouverte", "ODC Open Database License"] },
    });
    await fireEvent.focus(getByRole("combobox"));
    const suggestions = getAllByRole("option");
    expect(suggestions.length).toBe(2);
    expect(suggestions[0]).toHaveTextContent("Licence Ouverte");
    expect(suggestions[1]).toHaveTextContent("ODC Open Database License");
  });

  test("should filter suggestions by input value", async () => {
    const { getByRole, getAllByRole } = render(LicenseField, {
      props: { suggestions: ["Licence Ouverte", "ODC Open Database License"] },
    });

    const input = getByRole("combobox");

    await fireEvent.focus(input);
    await fireEvent.input(input, { target: { value: "ouv" } });
    expect(input).toHaveValue("ouv");

    const suggestions = getAllByRole("option");
    expect(suggestions.length).toBe(1);
    expect(suggestions[0]).toHaveTextContent("Licence Ouverte");
  });

  test("should choose a suggestion", async () => {
    const { getByRole, getAllByRole, component } = render(LicenseField, {
      props: { suggestions: ["Licence Ouverte", "ODC Open Database License"] },
    });

    const input = getByRole("combobox");
    await fireEvent.focus(input);

    const suggestions = getAllByRole("option");
    expect(suggestions.length).toBe(2);

    await fireEvent.click(suggestions[0]);

    const value = await new Promise<string>((resolve) => {
      component.$on("input", (event) => resolve(event.detail));
    });

    expect(value).toBe("Licence Ouverte");
  });

  test("should show error", async () => {
    const { getByRole } = render(LicenseField, {
      props: { error: "Unexpected error" },
    });
    const input = getByRole("combobox");
    expect(input).toHaveAccessibleDescription("Unexpected error");
  });
});
