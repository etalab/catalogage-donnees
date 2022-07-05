<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasets } from "$lib/repositories/datasets";
  import { apiToken } from "$lib/stores/auth";
  import { getPageFromParams } from "$lib/util/pagination";

  export const load: Load = async ({ fetch, url }) => {
    const page = getPageFromParams(url.searchParams);
    const q = url.searchParams.get("q") || "";

    const paginatedDatasets = await getDatasets({
      fetch,
      apiToken: get(apiToken),
      page,
      q,
    });

    return {
      props: {
        paginatedDatasets,
        currentPage: page,
        q,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import { page as pageStore } from "$app/stores";
  import type { Dataset } from "src/definitions/datasets";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { patchQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";
  import { makePageParam } from "$lib/util/pagination";
  import type { Paginated } from "src/definitions/pagination";
  import PaginationContainer from "./_PaginationContainer.svelte";

  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let currentPage: number;
  export let q: string;

  const updateSearch = (event: CustomEvent<string>) => {
    const href = patchQueryString($pageStore.url.searchParams, [
      ["q", event.detail],
      // If on page n = (2, ...), go back to page 1 on new search.
      makePageParam(1),
    ]);
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

<section class="fr-container">
  <div class="fr-grid-row">
    <div class="fr-col-12">
      {#if Maybe.Some(paginatedDatasets)}
        {#if q}
          <h2 class="fr-mb-3w">
            {paginatedDatasets.totalItems}
            {pluralize(paginatedDatasets.totalItems, "résultat", "résultats")}
          </h2>
        {/if}

        <DatasetList datasets={paginatedDatasets.items} />

        <PaginationContainer
          {currentPage}
          totalPages={paginatedDatasets.totalPages}
        />
      {/if}
    </div>
  </div>
</section>
