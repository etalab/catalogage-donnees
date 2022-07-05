<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import {
    getDatasets,
    getDatasetSearchFilters,
  } from "$lib/repositories/datasets";
  import { apiToken } from "$lib/stores/auth";
  import { page as pageStore } from "$app/stores";

  export const load: Load = async ({ fetch, url }) => {
    const page = +(url.searchParams.get("page") || 1);

    const token = get(apiToken);

    const q = url.searchParams.get("q") || "";
    const [paginatedDatasets, searchFilters] = await Promise.all([
      getDatasets({
        fetch,
        apiToken: token,
        page: 1,
        q,
      }),
      getDatasetSearchFilters({ fetch, apiToken: token }),
    ]);

    if (!searchFilters) {
      return {
        props: {
          paginatedDatasets,
          searchFilters: null,
          currentPage: page,
          q,
        },
      };
    }

    return {
      props: {
        paginatedDatasets,
        searchFilters,
        currentPage: page,
        q,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type {
    Dataset,
    DatasetFilters,
    SelectableDatasetFilter,
  } from "src/definitions/datasets";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { patchQueryString, toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";
  import {
    cleanSearchDatasetFilters,
    mergeSelectableDatasetFilter,
  } from "src/lib/util/dataset";
  import type { GetPageLink, Paginated } from "src/definitions/pagination";
  import FilterPanel from "./_FilterPanel.svelte";
  import PaginationContainer from "./_PaginationContainer.svelte";

  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let q: string;
  export let currentPage: number;

  export let searchFilters: Maybe<DatasetFilters>;

  let selectedFilters: Partial<SelectableDatasetFilter>;

  let displayFilters = false;

  const updateSearch = async (event: CustomEvent<string>) => {
    q = event.detail;

    if (!q) {
      const href = `search`; // Same page, remove query string
      await goto(href);
      return;
    }

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

  const handleSelectedFilter = async (
    e: CustomEvent<SelectableDatasetFilter>
  ) => {
    selectedFilters = cleanSearchDatasetFilters(
      mergeSelectableDatasetFilter(selectedFilters, e.detail)
    );

    paginatedDatasets = await getDatasets({
      fetch,
      page: currentPage,
      apiToken: $apiToken,
      filters: selectedFilters,
      q,
    });
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
  {#if Maybe.Some(paginatedDatasets)}
    <div class="fr-grid-row summary">
      <div class="fr-col-12 fr-pb-3w summary__header">
        <h2>
          {paginatedDatasets.totalItems}
          {pluralize(paginatedDatasets.totalItems, "résultat", "résultats")}
        </h2>

        <button
          on:click={() => (displayFilters = !displayFilters)}
          class="fr-btn fr-btn--secondary  fr-btn--icon-right {!displayFilters
            ? 'fr-icon-arrow-down-s-line'
            : 'fr-icon-arrow-up-s-line'}"
        >
          Affiner la recherche
        </button>
      </div>
    </div>

    {#if searchFilters}
      <div
        data-testid="dataset-filters"
        class="fr-grid-row fr-grid-row--gutters fr-py-3w {!displayFilters
          ? 'hidden'
          : undefined} filters"
      >
        <FilterPanel on:change={handleSelectedFilter} filters={searchFilters} />
      </div>
    {/if}

    <div class="fr-grid-row">
      <div class="fr-col-12">
        <DatasetList datasets={paginatedDatasets.items} />
        <PaginationContainer
          {getPageLink}
          totalPages={paginatedDatasets.totalItems}
          {currentPage}
        />
      </div>
    </div>
  {/if}
</section>

<style>
  .summary__header {
    border-bottom: 1px solid var(--border-default-grey);
  }
  .pagination-container {
    display: flex;
    justify-content: space-around;
  }

  h2 {
    padding: 0;
  }

  .hidden {
    display: none;
    height: 0;
  }

  .filters {
    border-bottom: 1px solid var(--border-default-grey);
    justify-content: space-between;
  }

  .summary__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
