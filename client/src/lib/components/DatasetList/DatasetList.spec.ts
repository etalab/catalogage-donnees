import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";

import DatasetList from "./DatasetList.svelte";
import type { Dataset } from "src/definitions/datasets";
import { getFakeDataset } from "src/tests/factories/dataset";

describe("Test the dataset list", () => {
  const fakeDatasets: Dataset[] = [
    getFakeDataset({
      id: "1",
    }),
    getFakeDataset({
      id: "2",
    }),
    getFakeDataset({
      id: "3",
    }),
  ];

  test("The list has the expected number of items", () => {
    const { getAllByRole } = render(DatasetList, {
      props: { datasets: fakeDatasets },
    });
    expect(getAllByRole("listitem")).toHaveLength(3);
  });
});
