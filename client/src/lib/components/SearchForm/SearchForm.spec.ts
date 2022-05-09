import "@testing-library/jest-dom";

import SearchForm from "./SearchForm.svelte";
import { render, fireEvent } from "@testing-library/svelte";

describe("Test the search form", () => {
  test("The form is marked as 'search'", () => {
    const { getByRole } = render(SearchForm);
    expect(getByRole("search")).toBeInTheDocument();
  });

  test("The 'search' field is present", () => {
    const { getByRole } = render(SearchForm);
    expect(getByRole("searchbox")).toBeInTheDocument();
  });

  test("The submit button is present", () => {
    const { getByRole } = render(SearchForm);
    expect(getByRole("button")).toBeInTheDocument();
  });

  test("The 'search' initial value can be set", async () => {
    const props = { value: "initial" };
    const { getByRole } = render(SearchForm, { props });
    const search = getByRole("searchbox") as HTMLInputElement;
    expect(search.value).toBe("initial");
  });

  test("The form submits the search value", async () => {
    const { getByRole, component } = render(SearchForm);

    const submittedValues: string[] = [];
    component.$on("submit", (event: CustomEvent<string>) => {
      submittedValues.push(event.detail);
    });

    await fireEvent.click(getByRole("button"));
    expect(submittedValues.pop()).toBe("");

    await fireEvent.input(getByRole("searchbox"), {
      target: { value: "Forêt" },
    });
    await fireEvent.click(getByRole("button"));
    expect(submittedValues.pop()).toBe("Forêt");
  });

  test("The form must be large", async () => {
    const { getByRole } = render(SearchForm);
    expect(getByRole("search")).toHaveClass("fr-search-bar--lg");
  });
});
