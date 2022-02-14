import type { Dataset } from "src/definitions/datasets";
import { API_PORT } from "src/env";
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
    expect(req.url).toEqual(`http://localhost:${API_PORT}/datasets/`);
    const body = JSON.stringify(datasetsMock);
    const headers = { "Content-Type": "application/json" };
    return new Response(body, { headers });
  };

  expect(await getDatasets({ fetch })).toEqual(datasetsMock);
});
