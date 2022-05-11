import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";
import type { GetPageLink } from "src/definitions/pagination";
import { range } from "$lib/util/array";

import Pagination from "./Pagination.svelte";

describe("Test the pagination", () => {
  const getPageLink: GetPageLink = (page) => `?page=${page}`;
  const hiddenOnMobile = (el: HTMLElement) =>
    el.classList.contains("fr-displayed-lg");

  test("The pagination is shown", () => {
    const props = { currentPage: 4, totalPages: 10, getPageLink };
    const { getByTestId } = render(Pagination, { props });
    expect(getByTestId("pagination-list")).toBeInTheDocument();
  });

  test.each(range(1, 5))(
    "The current page is always showcased and not clickable",
    (currentPage) => {
      const props = { currentPage, totalPages: 4, getPageLink };
      const { getByTitle } = render(Pagination, { props });
      const currentPageEl = getByTitle(`Page ${currentPage}`);
      expect(currentPageEl).toBeInTheDocument();
      expect(currentPageEl).toHaveAttribute("aria-current", "page");
      expect(currentPageEl).not.toHaveAttribute("href");
      expect(hiddenOnMobile(currentPageEl)).toBeFalsy();
    }
  );

  describe("Quick navigation controls", () => {
    test("The controls are shown", () => {
      const props = { currentPage: 4, totalPages: 10, getPageLink };
      const { getByRole } = render(Pagination, { props });

      const firstPage = getByRole("link", { description: "Première page" });
      expect(firstPage).toBeInTheDocument();
      expect(firstPage).toHaveAttribute("href", "?page=1");
      expect(hiddenOnMobile(firstPage)).toBeFalsy();

      const previousPage = getByRole("link", {
        description: "Page précédente",
      });
      expect(previousPage).toBeInTheDocument();
      expect(previousPage).toHaveAttribute("href", "?page=3");
      expect(hiddenOnMobile(previousPage)).toBeFalsy();

      const nextPage = getByRole("link", { description: "Page suivante" });
      expect(nextPage).toBeInTheDocument();
      expect(nextPage).toHaveAttribute("href", "?page=5");
      expect(hiddenOnMobile(nextPage)).toBeFalsy();

      const lastPage = getByRole("link", { description: "Dernière page" });
      expect(lastPage).toBeInTheDocument();
      expect(lastPage).toHaveAttribute("href", "?page=10");
      expect(hiddenOnMobile(lastPage)).toBeFalsy();
    });

    test("The first and previous page controls are disabled on first page", () => {
      const props = { currentPage: 2, totalPages: 3, getPageLink };
      const { getByRole, getByText, rerender } = render(Pagination, { props });
      expect(
        getByRole("link", { description: "Première page" })
      ).not.toHaveAttribute("aria-disabled");
      expect(
        getByRole("link", { description: "Page précédente" })
      ).not.toHaveAttribute("aria-disabled");

      rerender({ props: { ...props, currentPage: 1 } });
      expect(getByText("Première page", { selector: "a" })).toHaveAttribute(
        "aria-disabled",
        "true"
      );
      expect(getByText("Page précédente", { selector: "a" })).toHaveAttribute(
        "aria-disabled",
        "true"
      );
    });

    test("The next and last page links are disabled on last page", () => {
      const props = { currentPage: 2, totalPages: 3, getPageLink };
      const { getByRole, getByText, rerender } = render(Pagination, { props });
      expect(
        getByRole("link", { description: "Page suivante" })
      ).not.toHaveAttribute("aria-disabled");
      expect(
        getByRole("link", { description: "Dernière page" })
      ).not.toHaveAttribute("aria-disabled");

      rerender({ props: { ...props, currentPage: 3 } });
      expect(getByText("Page suivante", { selector: "a" })).toHaveAttribute(
        "aria-disabled",
        "true"
      );
      expect(getByText("Dernière page", { selector: "a" })).toHaveAttribute(
        "aria-disabled",
        "true"
      );
    });
  });

  describe("Large paginations", () => {
    test.each(range(2, 9))(
      "First and last pages are always shown - Page %s",
      (currentPage) => {
        const props = { currentPage, totalPages: 9, getPageLink };
        const { getByRole } = render(Pagination, { props });

        const firstPage = getByRole("link", { description: "Page 1" });
        expect(firstPage).toBeInTheDocument();
        expect(firstPage).toHaveAttribute("href", "?page=1");
        expect(hiddenOnMobile(firstPage)).toBeFalsy();
        
        const lastPage = getByRole("link", { description: "Page 9" });
        expect(lastPage).toBeInTheDocument();
        expect(lastPage).toHaveAttribute("href", "?page=9");
        expect(hiddenOnMobile(lastPage)).toBeFalsy();
      }
    );

    test("The current page is surrounded by 2 siblings", () => {
      const props = { currentPage: 5, totalPages: 9, getPageLink };
      const { queryAllByRole } = render(Pagination, { props });

      const pages = queryAllByRole("link", { description: /Page [2-8]/i });
      expect(pages).toHaveLength(4);
      expect(pages[0]).toHaveAccessibleDescription("Page 3");
      expect(pages[0]).toHaveAttribute("href", "?page=3");
      expect(hiddenOnMobile(pages[0])).toBeTruthy();
      expect(pages[1]).toHaveAccessibleDescription("Page 4");
      expect(pages[1]).toHaveAttribute("href", "?page=4");
      expect(hiddenOnMobile(pages[1])).toBeTruthy();
      expect(pages[2]).toHaveAccessibleDescription("Page 6");
      expect(pages[2]).toHaveAttribute("href", "?page=6");
      expect(hiddenOnMobile(pages[2])).toBeTruthy();
      expect(pages[3]).toHaveAccessibleDescription("Page 7");
      expect(pages[3]).toHaveAttribute("href", "?page=7");
      expect(hiddenOnMobile(pages[3])).toBeTruthy();
    });

    test("No truncature is shown below 3 page distance to start or end", () => {
      const props = { currentPage: 1, totalPages: 4, getPageLink };
      const { queryByText, rerender } = render(Pagination, { props });
      expect(queryByText("...")).not.toBeInTheDocument();
      rerender({ props: { ...props, currentPage: 4 } });
      expect(queryByText("...")).not.toBeInTheDocument();
    });

    test("Single truncature is shown beyond 4 page distance to start or end", () => {
      const props = { currentPage: 1, totalPages: 5, getPageLink };
      const { getByTestId, rerender } = render(Pagination, { props });
      expect(getByTestId("right-truncature")).toBeInTheDocument();
      rerender({ props: { ...props, currentPage: 5 } });
      expect(getByTestId("left-truncature")).toBeInTheDocument();
    });

    test("Both truncatures are shown beyond 4 page distance to start and end", () => {
      const props = { currentPage: 5, totalPages: 9, getPageLink };
      const { getByTestId } = render(Pagination, { props });
      expect(getByTestId("left-truncature")).toBeInTheDocument();
      expect(getByTestId("right-truncature")).toBeInTheDocument();
    });
  });
});
