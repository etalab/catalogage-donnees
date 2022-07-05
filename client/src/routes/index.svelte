<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { apiToken } from "$lib/stores/auth";
  import { getDatasets } from "$lib/repositories/datasets";
  import { getPageFromParams } from "$lib/util/pagination";

  export const load: Load = async ({ fetch, url }) => {
    const page = getPageFromParams(url.searchParams);

    const paginatedDatasets = await getDatasets({
      fetch,
      apiToken: get(apiToken),
      page,
    });

    return {
      props: {
        paginatedDatasets,
        currentPage: page,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { Dataset } from "src/definitions/datasets";
  import type { Paginated } from "src/definitions/pagination";
  import { toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import paths from "$lib/paths";
  import PaginationContainer from "./fiches/_PaginationContainer.svelte";

  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let currentPage: number;

  const submitSearch = (event: CustomEvent<string>) => {
    const q = event.detail;
    const queryString = toQueryString([["q", q]]);
    const href = `${paths.datasetSearch}${queryString}`;
    goto(href);
  };
</script>

<svelte:head>
  <title>Catalogue</title>
</svelte:head>

<section class="fr-background-alt--grey fr-mb-6w">
  <div class="fr-container fr-grid-row fr-grid-row--center fr-py-6w">
    <div class="fr-col-10">
      <h1>Recherchez un jeu de données</h1>
      <SearchForm on:submit={submitSearch} />
    </div>
  </div>
</section>

<section class="fr-container">
  <div class="fr-grid-row">
    <div class="fr-col-12">
      {#if Maybe.Some(paginatedDatasets)}
        <h2 class="fr-mb-3w">
          {paginatedDatasets.totalItems} jeux de donnnées contribués
        </h2>

        <DatasetList datasets={paginatedDatasets.items} />

        <PaginationContainer
          {currentPage}
          totalPages={paginatedDatasets.totalPages}
        />
      {/if}
    </div>
  </div>
</section>
