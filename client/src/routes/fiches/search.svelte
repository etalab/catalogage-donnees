<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasets } from "$lib/repositories/datasets";
  import { apiToken } from "$lib/stores/auth";

  export const load: Load = async ({ fetch, url }) => {
    const q = url.searchParams.get("q") || "";

    const datasets = await getDatasets({
      fetch,
      apiToken: get(apiToken),
      q,
    });

    return {
      props: {
        q,
        datasets,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { Dataset } from "src/definitions/datasets";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";

  export let q: string;
  export let datasets: Maybe<Dataset[]>;

  const updateSearch = (event: CustomEvent<string>) => {
    const q = event.detail;
    const queryString = toQueryString([["q", q]]);
    const href = `${queryString}`; // Same page, update query string only
    goto(href);
  };
</script>

<svelte:head>
  <title>Rechercher un jeu de données</title>
</svelte:head>
<section class="fr-background-alt--grey fr-mb-6w">
  <div class="fr-container fr-grid-row fr-grid-row--center fr-py-6w">
    <div class="fr-col-10">
      <h1>Recherchez un jeu de données</h1>
      <SearchForm value={q} on:submit={updateSearch} />
    </div>
  </div>
</section>

<section class="fr-container fr-mt-8w fr-mb-15w">
  {#if Maybe.Some(datasets)}
    {#if q}
      <h2 class="fr-mb-3w">
        {datasets.length}
        {pluralize(datasets.length, "résultat", "résultats")}
      </h2>
    {/if}
    <DatasetList {datasets} />
  {/if}
</section>
