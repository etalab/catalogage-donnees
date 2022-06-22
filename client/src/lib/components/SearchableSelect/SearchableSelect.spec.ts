/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import SearchableSelect from "./SearchableSelect.svelte";
import { render, fireEvent } from "@testing-library/svelte";
import type { SelectOption } from "src/definitions/form";
const buttonPlaceholder = "My button";
const inputPlaceholder = "My input";

const selectOptions: Array<SelectOption> = [
  {
    label: "un arbre",
    value: "arbre",
  },
  {
    label: "une plante",
    value: "plante",
  },
];

const props = {
  inputPlaceholder,
  buttonPlaceholder,
  options: selectOptions,
};

describe("Test the dataset form", () => {
  test("must have a button with placeholder", () => {
    const { getByRole } = render(SearchableSelect, {
      props,
    });
    const button = getByRole("button");

    expect(button).toHaveTextContent(buttonPlaceholder);
  });

  test("should not display the dropdown until the button has been clicked", () => {
    const { queryByRole } = render(SearchableSelect, {
      props,
    });
    const list = queryByRole("list");

    expect(list).toBeNull();
  });

  test("a dropdown must be displayed after button click", async () => {
    const { getByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");

    await fireEvent.click(button);
    const list = getByRole("list");

    expect(list).not.toBeNull();
  });

  test("a dropdown must display options label", async () => {
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const options = getAllByRole("listitem");
    expect(options[0].textContent).toBe(selectOptions[0].label);
  });

  test("should have a text input of type search", async () => {
    const { getByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");
    expect(input).toHaveAttribute("type", "search");
  });

  test("should filter options according to search term", async () => {
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");

    await fireEvent.input(input, {
      target: { value: "arbre" },
    });

    const options = getAllByRole("listitem");
    expect(options.length).toBe(2);
  });

  test("the search should be case insensitive", async () => {
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");

    await fireEvent.input(input, {
      target: { value: "ArBre" },
    });

    const options = getAllByRole("listitem");
    expect(options.length).toBe(2);
    expect(options[0].textContent).toBe("un arbre");
  });

  test("a message telling no result has been found must be display if ... no result has been found", async () => {
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");

    await fireEvent.input(input, {
      target: { value: "yolo" },
    });

    const options = getAllByRole("listitem");
    expect(options.length).toBe(1);

    expect(options[0].textContent).toBe("Aucun résultat trouvé");
  });

  test("the button should display the selected item value", async () => {
    const searchTerm = "arbre";
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");

    await fireEvent.input(input, {
      target: { value: searchTerm },
    });

    const options = getAllByRole("listitem");

    await fireEvent.click(options[0]);

    expect(button).toHaveTextContent("un arbre");
  });

  test("the selected option must be displayed", async () => {
    const searchTerm = "arbre";
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");

    await fireEvent.input(input, {
      target: { value: searchTerm },
    });

    const options = getAllByRole("listitem");

    await fireEvent.click(options[0]);

    expect(button).toHaveTextContent("un arbre");
  });

  test("should hide the overlay after an item has been clicked", async () => {
    const searchTerm = "arbre";
    const { getByRole, getAllByRole } = render(SearchableSelect, {
      props,
    });

    const button = getByRole("button");
    await fireEvent.click(button);
    const input = getByRole("searchbox");

    await fireEvent.input(input, {
      target: { value: searchTerm },
    });

    const options = getAllByRole("listitem");

    await fireEvent.click(options[0]);

    expect(input).not.toBeVisible();
  });
});
