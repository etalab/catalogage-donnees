import "@testing-library/jest-dom";

import Search from "./SearchBar.svelte";
import { render, fireEvent } from "@testing-library/svelte";

describe("Test the search form", () => {
  test("The form is marked as 'search'", () => {
    const { getByRole } = render(Search);
    expect(getByRole("search")).toBeInTheDocument();
  });

  test("The 'search' field is present", () => {
    const { getByRole } = render(Search);
    expect(getByRole("searchbox")).toBeInTheDocument();
  });

  test("The submit button is present", () => {
    const { getByRole } = render(Search);
    expect(getByRole("button")).toBeInTheDocument();
  });

  test("The 'search' initial value can be set", async () => {
    const props = { value: "initial" };
    const { getByRole } = render(Search, { props });
    const search = getByRole("searchbox") as HTMLInputElement;
    expect(search.value).toBe("initial");
  });

  test("The 'search' placeholder can be set", async () => {
    const { getByPlaceholderText, rerender } = render(Search);
    expect(getByPlaceholderText("Rechercher")).toBeInTheDocument();

    const props = { placeholder: "Rechercher un jeu de données" };
    rerender({ props });
    expect(
      getByPlaceholderText("Rechercher un jeu de données")
    ).toBeInTheDocument();
  });

  test("The form submits the search value", async () => {
    const { getByRole, getByPlaceholderText, component } = render(Search);

    const submittedValues: string[] = [];
    component.$on("submit", (event: CustomEvent<string>) => {
      submittedValues.push(event.detail);
    });

    await fireEvent.click(getByRole("button"));
    expect(submittedValues.pop()).toBe("");

    const input = getByPlaceholderText("Rechercher");

    await fireEvent.input(input, {
      target: { value: "Forêt" },
    });

    await fireEvent.click(getByRole("button"));
    expect(submittedValues.pop()).toBe("Forêt");
  });

  test("The form can be large", async () => {
    const { getByRole, rerender } = render(Search);
    expect(getByRole("search")).not.toHaveClass("fr-search-bar--lg");

    const props = { size: "lg" };
    rerender({ props });
    expect(getByRole("search")).toHaveClass("fr-search-bar--lg");
  });
});
