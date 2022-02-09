<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { getDatasets } from "$lib/repositories/datasets";

  export const load: Load = async ({ fetch }) => {
    const datasets = await getDatasets({ fetch });
    return {
      props: {
        datasets,
      },
    };
  };
</script>

<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";

  export let datasets: Dataset[];
</script>

<svelte:head>
  <title>Catalogue</title>
</svelte:head>

<h2>Dernières contributions</h2>

<section>
  <DatasetList {datasets} />
</section>
