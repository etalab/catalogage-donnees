import "@testing-library/jest-dom";

import Search from "./Search.svelte";
import { render, fireEvent, screen } from "@testing-library/svelte";

describe("Test the Search", () => {
  test("should return the selected option", async () => {
    const { getByRole, component } = render(Search, {
      label: "label",
      name: "my-list",
      options: [
        {
          label: "foo",
          value: "value",
        },
        {
          label: "tata",
          value: "toto",
        },
      ],
    });

    type SelectOption = {
      label: string;
      value: string;
    };
    let option: SelectOption;

    component.$on("search", (e: CustomEvent<SelectOption>) => {
      option = e.detail;
    });

    const input = getByRole("search");

    await fireEvent.input(input, {
      target: {
        value: "tata",
      },
    });

    expect(option).toEqual({
      label: "tata",
      value: "toto",
    });
  });

  test("should NOT return the selected option if no matching option found", async () => {
    const { getByRole, component } = render(Search, {
      label: "label",
      name: "my-list",
      options: [
        {
          label: "foo",
          value: "value",
        },
        {
          label: "tata",
          value: "toto",
        },
      ],
    });

    type SelectOption = {
      label: string;
      value: string;
    };
    let option: SelectOption;

    component.$on("search", (e: CustomEvent<SelectOption>) => {
      option = e.detail;
    });

    const input = getByRole("search");

    await fireEvent.input(input, {
      target: {
        currentValue: "lol",
      },
    });

    expect(option).toBeUndefined();
  });
});
