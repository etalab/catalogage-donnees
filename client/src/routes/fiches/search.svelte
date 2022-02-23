<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { getDatasets } from "$lib/repositories/datasets";

  export const load: Load = async ({ fetch, url }) => {
    const q = url.searchParams.get("q") || "";
    const datasets = await getDatasets({ fetch, q });
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
  import { pluralize, toQueryString } from "$lib/util";

  export let q: string;
  export let datasets: Dataset[];

  const updateSearch = () => {
    const queryString = toQueryString([["q", q]]);
    const href = `?${queryString}`;
    goto(href);
  };
</script>

<section class="fr-container fr-mt-9w">
  <div class="fr-col-6">
    <h2>Rechercher un jeu de données</h2>

    <form
      class="fr-search-bar"
      role="search"
      on:submit|preventDefault={updateSearch}
    >
      <label for="q" class="fr-label"> Votre recherche </label>
      <input
        type="search"
        class="fr-input"
        name="q"
        bind:value={q}
        placeholder="Rechercher"
      />
      <button type="submit" class="fr-btn"> Rechercher </button>
    </form>
  </div>

  <h4 class="fr-mt-6w">
    {datasets.length}
    {pluralize(datasets.length, "résultat", "résultats")}
  </h4>

  <DatasetList {datasets} />
</section>
