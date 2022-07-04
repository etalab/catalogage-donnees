<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasets } from "$lib/repositories/datasets";
  import { apiToken } from "$lib/stores/auth";

  export const load: Load = async ({ fetch, url }) => {
    const page = +(url.searchParams.get("page") || 1);
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
  import { patchQueryString, toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";
  import type { GetPageLink, Paginated } from "src/definitions/pagination";
  import PaginationContainer from "./_PaginationContainer.svelte";

  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let currentPage: number;
  export let q: string;

  const updateSearch = (event: CustomEvent<string>) => {
    q = event.detail;
    const queryString = toQueryString([["q", q]]);
    const href = `${queryString}`; // Same page, update query string only
    goto(href);
  };

  const getPageLink: GetPageLink = (page) => {
    const queryString = patchQueryString($pageStore.url.searchParams, [
      ["page", page.toString()],
    ]);
    return `${queryString}`;
  };
</script>

<svelte:head>
  <title>Rechercher un jeu de données</title>
</svelte:head>
<section class="fr-background-alt--grey fr-mb-6w">
  <div class="fr-container fr-grid-row fr-grid-row--center fr-py-6w">
    <div class="fr-col-10">
      <h1>Recherchez un jeu de données</h1>
      <SearchForm on:submit={updateSearch} />
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
          {getPageLink}
          totalPages={paginatedDatasets.totalPages}
          {currentPage}
        />
      {/if}
    </div>
  </div>
</section>
