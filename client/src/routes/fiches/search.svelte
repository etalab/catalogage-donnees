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
  import { pluralize } from "$lib/util/format";
  import { toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";

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

{#if Maybe.Some(datasets)}
  <section class="fr-container fr-mt-9w">
    <div class="fr-col-6">
      <h2>Rechercher un jeu de données</h2>

      <SearchForm value={q} on:submit={updateSearch} />
    </div>

    {#if datasets.length > 0}
      <h4 class="fr-mt-6w">
        {datasets.length}
        {pluralize(datasets.length, "résultat", "résultats")}
      </h4>
    {/if}

    <DatasetList {datasets} />
  </section>
{/if}
