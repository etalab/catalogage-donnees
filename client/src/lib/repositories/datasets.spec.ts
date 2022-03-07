import type { Dataset } from "src/definitions/datasets";
import type { Fetch } from "src/definitions/fetch";
import { getDatasets } from "./datasets";

test("The datasets endpoint behaves as expected", async () => {
  const fakeDatasets: Dataset[] = [
    {
      id: "uuid1",
      title: "Inventaire des arbres et forêts",
      description: "Fichier de l'ensemble des arbres et forêts de France.",
      formats: ["database"],
    },
  ];

  const fakeFetch: Fetch = async (request) => {
    expect(request.method).toBe("GET");
    expect(new URL(request.url, "http://test").pathname).toBe("/datasets/");

    const body = JSON.stringify(fakeDatasets);
    const headers = { "Content-Type": "application/json" };
    return new Response(body, { headers });
  };

  const datasets = await getDatasets({ fetch: fakeFetch });

  expect(datasets).toEqual(fakeDatasets);
});
