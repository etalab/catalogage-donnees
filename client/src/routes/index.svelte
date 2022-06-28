<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { apiToken } from "$lib/stores/auth";
  import { getDatasets, getSearchFilter } from "$lib/repositories/datasets";

  export const load: Load = async ({ fetch, url }) => {
    const page = +(url.searchParams.get("page") || 1);

    const token = get(apiToken);

    // Promise.all?

    const paginatedDatasets = await getDatasets({
      fetch,
      apiToken: token,
      page,
    });

    const searchFilters = await getSearchFilter(fetch, token);

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

  const handleSelectedFilter = (e: CustomEvent<SelectableSearchFilter>) => {
    selectedFilters = cleanSearchFilters(
      mergeSelectableSearchFilter(selectedFilters, e.detail)
    );

    const queryParamsRecords = toSearchQueryParamRecord(selectedFilters);

    const queryString = patchQueryString(
      $pageStore.url.searchParams,
      queryParamsRecords
    );

    console.log(queryString);
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
  {#if groupedSearchFilters}
    <div class="fr-grid-row fr-grid-row--center fr-grid-row--gutters fr-mb-3w">
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
      {#if Maybe.Some(paginatedDatasets)}
        <h2 class="fr-mb-3w">
          {paginatedDatasets.totalItems} jeux de donnnées contribués
        </h2>

        <DatasetList datasets={paginatedDatasets.items} />
        <div class="pagination-container fr-mt-2w ">
          <Pagination
            {currentPage}
            totalPages={paginatedDatasets.totalPages}
            {getPageLink}
          />
        </div>
      {/if}
    </div>
  </div>
</section>

<style>
  .pagination-container {
    display: flex;
    justify-content: space-around;
  }

  /* Filters */

  p {
    padding: 0;
  }
</style>
