import "@testing-library/jest-dom";
import { render } from "@testing-library/svelte";

import DatasetList from "./DatasetList.svelte";
import type { Dataset } from "src/definitions/datasets";
import { getFakeDataSet } from "src/fixtures/dataset";

describe("Test the dataset list", () => {
  const now = new Date();
  const fakeDatasets: Dataset[] = [
    getFakeDataSet({
      id: "uuid1",
      createdAt: now,
      title: "Inventaire des arbres et forêts",
      description: "Fichier de l'ensemble des arbres et forêts de France.",
      formats: ["database"],
      entrypointEmail: "forets@ign.fr",
    }),
    getFakeDataSet({
      id: "uuid2",
      createdAt: now,
      title: "Bureaux de vote Hauts-de-France",
      description:
        "Fichier JSON des bureaux de vote de l'ensemble des circonscriptions de la région Hauts-de-France.",
      formats: ["api"],
      entrypointEmail: "citoyennete@hautsdefrance.fr",
    }),
    getFakeDataSet({
      id: "uuid3",
      createdAt: now,
      title: "Masse salariale du secteur privé",
      description:
        "Masse salariale telle que calculée par l'Urssaf et publiée dans le Baromètre économique.",
      formats: ["file_tabular"],
      entrypointEmail: "statistiques@urssaf.gouv.fr",
    }),
  ];

  test("The list has the expected number of items", () => {
    const { getAllByRole } = render(DatasetList, {
      props: { datasets: fakeDatasets },
    });
    expect(getAllByRole("listitem")).toHaveLength(3);
  });
});
