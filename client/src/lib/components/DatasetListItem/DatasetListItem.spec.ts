import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";

import DatasetListItem from "./DatasetListItem.svelte";
import type { Dataset } from "src/definitions/datasets";

describe("Test the dataset list item", () => {
  const fakeDatasets: Dataset = {
    id: "uuid1",
    title: "Inventaire des arbres et forêts",
    description: "Fichier de l'ensemble des arbres et forêts de France.",
    formats: ["database"],
  };

  test("The title is present", () => {
    const { getByText } = render(DatasetListItem, {
      props: { dataset: fakeDatasets },
    });
    expect(getByText("Inventaire des arbres et forêts")).toBeInTheDocument();
  });

  test("The detail link is present", () => {
    const { getByRole } = render(DatasetListItem, {
      props: { dataset: fakeDatasets },
    });
    expect(getByRole("link")).toBeInTheDocument();
  });

  test("The detail link points to detail page", () => {
    const { getByRole } = render(DatasetListItem, {
      props: { dataset: fakeDatasets },
    });
    const detailLink = getByRole("link");
    expect(detailLink).toHaveTextContent("Voir");
    expect(detailLink).toHaveAttribute("href", "/fiches/uuid1");
    expect(detailLink).toHaveAttribute("title");
  });
});
