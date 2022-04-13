import { fireEvent } from "@testing-library/dom";
import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";
import type { SelectOption } from "src/definitions/selectOption";
import Select from "./Select.svelte";

describe("Test the select component", () => {
  test("should display a select input with 3 options", () => {
    const options: SelectOption[] = [
      {
        label: "label-1",
        value: "value-1",
      },
      {
        label: "label-2",
        value: "value-2",
      },
      {
        label: "label-3",
        value: "value-3",
      },
    ];

    const placeholder = "My brand new select";

    const props = {
      placeholder,
      options,
      label: "My Nice Select",
      id: "myId",
      name: "mySelect",
    };

    const { getAllByRole } = render(Select, { props });

    expect(getAllByRole("option").length).toBe(4);
  });

  test("should have a default option selected", () => {
    const options: SelectOption[] = [];

    const placeholder = "My brand new select";

    const props = {
      placeholder,
      options,
      label: "My Nice Select",
      id: "myId",
      name: "mySelect",
    };

    const { getByRole } = render(Select, { props });

    expect(
      (getByRole("option", { name: placeholder }) as HTMLOptionElement).selected
    ).toBeTruthy();
  });

  test("should be marked as required", () => {
    const options: SelectOption[] = [];

    const placeholder = "My brand new select";
    const label = "label";

    const props = {
      placeholder,
      options,
      label,
      id: "myId",
      name: "mySelect",
      required: true,
    };

    const { getByLabelText } = render(Select, { props });

    const labelInput = getByLabelText(label, {
      exact: false,
    });
    expect(labelInput).toBeDefined();
    expect(labelInput.children).toHaveLength(1);
  });

  test("on:change should be triggered", () => {
    const options: SelectOption[] = [
      {
        label: "label",
        value: "my-name",
      },
    ];
    const label = "label";

    const props = {
      options,
      label,
      id: "myId",
      name: "mySelect",
    };

    const { getByRole, component } = render(Select, { props });

    let count = 0;

    const mock = () => (count += 1);

    const option = getByRole("option", { name: "label" }) as HTMLOptionElement;

    component.$on("change", mock);
    fireEvent.change(option);

    expect(count).toBe(1);
  });
});
