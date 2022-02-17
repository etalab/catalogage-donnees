import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";

import DatasetList from "./DatasetList.svelte";
import type { Dataset } from "src/definitions/datasets";

describe("Test the dataset list", () => {
  const fakeDatasets: Dataset[] = [
    {
      id: "uuid1",
      title: "Inventaire des arbres et forêts",
      description: "Fichier de l'ensemble des arbres et forêts de France.",
    },
    {
      id: "uuid2",
      title: "Bureaux de vote Hauts-de-France",
      description:
        "Fichier JSON des bureaux de vote de l'ensemble des circonscriptions de la région Hauts-de-France.",
    },
    {
      id: "uuid3",
      title: "Masse salariale du secteur privé",
      description:
        "Masse salariale telle que calculée par l'Urssaf et publiée dans le Baromètre économique.",
    },
  ];

  test("The list has the expected number of items", () => {
    const { getAllByRole } = render(DatasetList, {
      props: { datasets: fakeDatasets },
    });
    expect(getAllByRole("listitem")).toHaveLength(3);
  });
});
