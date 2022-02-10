/**
 * @jest-environment jsdom
 */

import "@testing-library/jest-dom";

import type { Dataset } from "src/definitions/datasets";
import { getDatasets } from "./datasets";

test("The datasets endpoint behaves as expected", async () => {
  const datasetsMock: Dataset[] = [
    {
      id: "uuid1",
      title: "Inventaire des arbres et forêts",
      description: "Fichier de l'ensemble des arbres et forêts de France.",
    },
  ];

  const fetch = async (req: Request) => {
    expect(req.url).toBe("/api/datasets/");
    const body = JSON.stringify(datasetsMock);
    return new Response(body, { headers: { "Content-Type": "application/json" } });
  }

  expect(await getDatasets({ fetch })).toEqual(datasetsMock);
});
