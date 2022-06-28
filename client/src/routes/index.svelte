<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { apiToken } from "$lib/stores/auth";
  import { getDatasets, getSearchFilter } from "$lib/repositories/datasets";

  export const load: Load = async ({ fetch, url }) => {
    const page = +(url.searchParams.get("page") || 1);

    const token = get(apiToken);

    const [paginatedDatasets, searchFilters] = await Promise.all([
      getDatasets({
        fetch,
        apiToken: token,
        page,
      }),
      getSearchFilter(fetch, token),
    ]);

    if (!searchFilters) {
      return {
        props: {
          paginatedDatasets,
          groupedSearchFilters: null,
          currentPage: page,
        },
      };
    }

    return {
      props: {
        paginatedDatasets,
        groupedSearchFilters: groupSelectableSearchFilterByCategory(
          transformSearchFiltersIntoSelectableSearchFilters(searchFilters)
        ),
        currentPage: page,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import { page as pageStore } from "$app/stores";
  import type {
    Dataset,
    SelectableSearchFilterGroup,
    SelectableSearchFilter,
  } from "src/definitions/datasets";
  import type { GetPageLink, Paginated } from "src/definitions/pagination";
  import { patchQueryString, toQueryString } from "$lib/util/urls";
  import { Maybe } from "$lib/util/maybe";
  import DatasetList from "$lib/components/DatasetList/DatasetList.svelte";
  import Pagination from "$lib/components/Pagination/Pagination.svelte";
  import SearchForm from "$lib/components/SearchForm/SearchForm.svelte";
  import paths from "$lib/paths";
  import FilterSection from "./_FilterSection.svelte";
  import {
    cleanSearchFilters,
    groupSelectableSearchFilterByCategory,
    mergeSelectableSearchFilter,
  } from "src/lib/util/dataset";
  import { toSearchQueryParamRecord } from "src/lib/transformers/searchFilter";
  import { transformSearchFiltersIntoSelectableSearchFilters } from "src/lib/transformers/dataset";

  export let paginatedDatasets: Maybe<Paginated<Dataset>>;
  export let currentPage: number;
  export let groupedSearchFilters: Maybe<SelectableSearchFilterGroup>;

  let selectedFilters: Partial<SelectableSearchFilter>;
  let displayFilters = false;

  const submitSearch = (event: CustomEvent<string>) => {
    const q = event.detail;
    const queryString = toQueryString([["q", q]]);
    const href = `${paths.datasetSearch}${queryString}`;
    goto(href);
  };

  const getPageLink: GetPageLink = (page) => {
    const queryString = patchQueryString($pageStore.url.searchParams, [
      ["page", page.toString()],
    ]);
    return `${queryString}`;
  };

  const handleSelectedFilter = async (
    e: CustomEvent<SelectableSearchFilter>
  ) => {
    selectedFilters = cleanSearchFilters(
      mergeSelectableSearchFilter(selectedFilters, e.detail)
    );

    const queryParamsRecords = toSearchQueryParamRecord(selectedFilters);
    paginatedDatasets = await getDatasets({
      fetch,
      page: currentPage,
      apiToken: $apiToken,
      filters: queryParamsRecords,
    });
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
  {#if Maybe.Some(paginatedDatasets)}
    <div class="fr-grid-row summary">
      <div class="fr-col-12 fr-pb-3w summary__header">
        <h2>
          {paginatedDatasets.totalItems} jeux de donnnées contribués
        </h2>

        <button
          on:click={() => (displayFilters = !displayFilters)}
          class="fr-btn fr-btn--secondary"
        >
          Affiner la recherche
        </button>
      </div>
    </div>

    {#if groupedSearchFilters}
      <div
        class="fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-py-3w {displayFilters
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
    border-top: 1px solid var(--border-default-grey);
  }

  .summary__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
