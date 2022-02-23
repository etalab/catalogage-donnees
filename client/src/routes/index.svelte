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
  import { goto } from "$app/navigation";
  import type { Dataset } from "src/definitions/datasets";
  import { toQueryString } from "$lib/util";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";

  export let datasets: Dataset[];

  let q: string;

  const submitSearch = () => {
    const queryString = toQueryString([["q", q]]);
    const href = `/fiches/search?${queryString}`;
    goto(href);
  };
</script>

<svelte:head>
  <title>Catalogue</title>
</svelte:head>

<section class="fr-background-alt--grey fr-mb-6w">
  <div class="fr-container fr-grid-row fr-grid-row--center fr-p-6w">
    <div class="fr-col-10">
      <h1>Recherchez un jeu de données</h1>
      <form
        class="fr-search-bar fr-search-bar--lg"
        role="search"
        on:submit|preventDefault={submitSearch}
      >
        <label for="q" class="fr-label"> Recherche </label>
        <input
          type="search"
          name="q"
          class="fr-input"
          bind:value={q}
          placeholder="Ex : taux de contamination COVID, nombre de naissances en France, ..."
        />
        <button class="fr-btn" type="submit"> Rechercher </button>
      </form>
    </div>
  </div>
</section>

<section class="fr-container">
  <h2 class="fr-my-3w">Dernières contributions</h2>

  <DatasetList {datasets} />
</section>
