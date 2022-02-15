import type { Dataset } from "src/definitions/datasets";
import type { Fetch } from "src/definitions/fetch";
import { API_PORT } from "src/env";
import { getDatasets } from "./datasets";

test("The datasets endpoint behaves as expected", async () => {
  const fakeDatasets: Dataset[] = [
    {
      id: "uuid1",
      title: "Inventaire des arbres et forêts",
      description: "Fichier de l'ensemble des arbres et forêts de France.",
    },
  ];

  const fakeFetch: Fetch = async (request) => {
    expect(request.method).toBe("GET");
    expect(request.url).toBe(`http://localhost:${API_PORT}/api/datasets/`);

    const body = JSON.stringify(fakeDatasets);
    const headers = { "Content-Type": "application/json" };
    return new Response(body, { headers });
  };

  const datasets = await getDatasets({ fetch: fakeFetch });

  expect(datasets).toEqual(fakeDatasets);
});
