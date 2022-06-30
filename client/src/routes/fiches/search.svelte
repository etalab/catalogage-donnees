<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasets, getSearchFilter } from "$lib/repositories/datasets";
  import { apiToken } from "$lib/stores/auth";
  import { page as pageStore } from "$app/stores";

  export const load: Load = async ({ fetch, url }) => {
    const page = +(url.searchParams.get("page") || 1);

    const token = get(apiToken);

    const q = url.searchParams.get("q") || "";
    const [paginatedDatasets, searchFilters] = await Promise.all([
      getDatasets({
        fetch,
        apiToken: get(apiToken),
        page: 1,
        q,
      }),
      getSearchFilter(fetch, token),
    ]);

    if (!searchFilters) {
      return {
        props: {
          paginatedDatasets,
          groupedSearchFilters: null,
          currentPage: page,
          q,
        },
      };
    }

    return {
      props: {
        paginatedDatasets,
        groupedSearchFilters: groupSelectableDatasetFilterByCategory(
          transformSearchFiltersIntoSelectableDatasetFilters(searchFilters)
        ),
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
    SelectableDatasetFilter,
    SelectableDatasetFilterGroup,
  } from "src/definitions/datasets";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import { patchQueryString, toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import { pluralize } from "src/lib/util/format";
  import {
    cleanSearchFilters,
    groupSelectableDatasetFilterByCategory,
    mergeSelectableDatasetFilter,
  } from "src/lib/util/dataset";
  import { transformSearchFiltersIntoSelectableDatasetFilters } from "src/lib/transformers/dataset";
  import FilterSection from "../_FilterSection.svelte";
  import Pagination from "src/lib/components/Pagination/Pagination.svelte";
  import { toSearchQueryParamRecord } from "src/lib/transformers/searchFilter";
  import type { GetPageLink, Paginated } from "src/definitions/pagination";

  export let q: string;
  export let currentPage: number;
  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let groupedSearchFilters: Maybe<SelectableDatasetFilterGroup>;

  let selectedFilters: Partial<SelectableDatasetFilter>;

  let displayFilters = false;

  const updateSearch = (event: CustomEvent<string>) => {
    q = event.detail;

    if (!q) {
      const href = ``; // Same page, remove query string
      goto(href);
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
    selectedFilters = cleanSearchFilters(
      mergeSelectableDatasetFilter(selectedFilters, e.detail)
    );

    const queryParamsRecords = toSearchQueryParamRecord(selectedFilters);
    paginatedDatasets = await getDatasets({
      fetch,
      page: currentPage,
      apiToken: $apiToken,
      filters: queryParamsRecords,
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
      <SearchForm value={q} on:submit={updateSearch} />
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

        {#if paginatedDatasets.totalItems > 1}
          <button
            on:click={() => (displayFilters = !displayFilters)}
            class="fr-btn fr-btn--secondary  fr-btn--icon-right {!displayFilters
              ? 'fr-icon-arrow-down-s-line'
              : 'fr-icon-arrow-up-s-line'}"
          >
            Affiner la recherche
          </button>
        {/if}
      </div>
    </div>

    {#if groupedSearchFilters}
      <div
        data-testid="dataset-filters"
        class="fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-py-3w {!displayFilters
          ? 'hidden'
          : undefined} filters"
      >
        {#each Object.keys(groupedSearchFilters) as filterCategory}
          <div class="fr-col-4">
            <FilterSection
              searchFilters={groupedSearchFilters[filterCategory]}
              sectionTitle={filterCategory}
              on:filterSelected={handleSelectedFilter}
            />
          </div>
        {/each}
      </div>
    {/if}

    <div class="fr-grid-row">
      <div class="fr-col-12">
        <DatasetList datasets={paginatedDatasets.items} />
        <div class="pagination-container fr-mt-2w ">
          <Pagination
            {currentPage}
            totalPages={paginatedDatasets.totalPages}
            {getPageLink}
          />
        </div>
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
  }

  .summary__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
