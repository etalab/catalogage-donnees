/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";

import DatasetFilterSection from "./DatasetFilterSection.svelte";
import { render } from "@testing-library/svelte";
import { getFakeSelectableDatasetFilter } from "src/tests/factories/dataset";

const props = {
  sectionTitle: "My Section",
  searchFilters: getFakeSelectableDatasetFilter(),
};

describe("Test the dataset form", () => {
  test("must have a section title", () => {
    const { getByRole } = render(DatasetFilterSection, {
      props,
    });

    const title = getByRole("heading");

    expect(title.textContent).toBe(props.sectionTitle);
  });

  test("must display multiple filters", () => {
    const { getAllByTestId } = render(DatasetFilterSection, {
      props,
    });

    const filters = getAllByTestId(new RegExp("label$"));
    const filtersNames = filters.map((item) => item.textContent);

    expect(filtersNames).toEqual([
      "Mots-clés",
      "Couverture géographique",
      "Service producteur de la donnée",
      "Système d’information source",
      "Formats de mise à disposition",
    ]);
  });
});
