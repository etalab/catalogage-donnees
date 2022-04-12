import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";

import DatasetListItem from "./DatasetListItem.svelte";
import type { DatasetHeadlines } from "src/definitions/datasets";
import { getFakeDataset } from "src/tests/factories/dataset";

describe("Test the dataset list item", () => {
  const dataset = getFakeDataset({
    id: "uuid1",
    createdAt: new Date(),
    title: "Inventaire des arbres et forêts",
    description: "Fichier de l'ensemble des arbres et forêts de France.",
  });

  test("The title is present", () => {
    const { getByText } = render(DatasetListItem, {
      props: { dataset },
    });
    expect(getByText("Inventaire des arbres et forêts")).toBeInTheDocument();
  });

  test("The detail link is present", () => {
    const { getByRole } = render(DatasetListItem, {
      props: { dataset },
    });
    expect(getByRole("link")).toBeInTheDocument();
  });

  test("The detail link points to detail page", () => {
    const { getByRole } = render(DatasetListItem, {
      props: { dataset },
    });
    const detailLink = getByRole("link");
    expect(detailLink).toHaveTextContent("Voir");
    expect(detailLink).toHaveAttribute("href", "/fiches/uuid1");
    expect(detailLink).toHaveAttribute("title");
  });

  test("Marked headlines replace regular title and description", () => {
    const headlines: DatasetHeadlines = {
      title: "Inventaire des arbres et <mark>forêts</mark>",
      description:
        "Fichier de l'ensemble des arbres et <mark>forêts</mark> de France.",
    };
    const props = { dataset: { ...dataset, headlines } };
    const { queryByText, getByTestId } = render(DatasetListItem, { props });

    const headlinesTitle = getByTestId("headlines-title");
    expect(headlinesTitle).toBeInTheDocument();
    expect(headlinesTitle.innerHTML).toEqual(headlines.title);

    const headlinesDescription = getByTestId("headlines-description");
    expect(headlinesDescription).toBeInTheDocument();
    expect(headlinesDescription.innerHTML).toEqual(
      `... ${headlines.description} ...`
    );

    expect(queryByText(dataset.title)).not.toBeInTheDocument();
    expect(queryByText(dataset.description)).not.toBeInTheDocument();
  });
});
