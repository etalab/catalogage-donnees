import "@testing-library/jest-dom";

import SearchInput from "./SearchInput.svelte";
import { render, fireEvent } from "@testing-library/svelte";
import type { SelectOption } from "src/definitions/form";

describe("Test the Search", () => {
  test("should return the selected option", async () => {
    const searchedOption = {
      label: "Architecture",
      value: "uuid-1",
    };
    const { getByRole, component } = render(SearchInput, {
      name: "my-list",
      options: [
        searchedOption,
        {
          label: "Maison",
          value: "uui-2",
        },
      ],
    });

    let option: SelectOption = {
      label: "",
      value: "",
    };

    component.$on("search", (e: CustomEvent<SelectOption>) => {
      option = e.detail;
    });

    const input = getByRole("search");

    await fireEvent.input(input, {
      target: {
        value: searchedOption.label,
      },
    });

    await fireEvent.keyPress(input, {
      key: "Enter",
    });

    expect(option).toEqual(searchedOption);
  });

  test("should NOT return the selected option if no matching option found", async () => {
    const searchedOption = {
      label: "Architecture",
      value: "architecture",
    };
    const { getByRole, component } = render(SearchInput, {
      name: "my-list",
      options: [
        searchedOption,
        {
          label: "Maison",
          value: "maison",
        },
      ],
    });

    let option: SelectOption = {
      label: "",
      value: "",
    };

    component.$on("search", (e: CustomEvent<SelectOption>) => {
      option = e.detail;
    });

    const input = getByRole("search");

    await fireEvent.input(input, {
      target: {
        value: "not-a-value",
      },
    });

    await fireEvent.keyDown(input, {
      key: "Enter",
    });

    expect(option).toEqual(option);
  });
});
