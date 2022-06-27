<script lang="ts">
  import { DATASET_FILTERS_TRANSLATION } from "src/constants";

  import type { SelectOption } from "src/definitions/form";
  import type { SearchFilter } from "src/definitions/datasets";
  import type { Tag } from "src/definitions/tag";

  import SearchableSelect from "src/lib/components/SearchableSelect/SearchableSelect.svelte";
  import { mergeSearchFilters } from "src/lib/util/dataset";
  import { createEventDispatcher } from "svelte";

  export let sectionTitle: string;
  export let searchFilters: SearchFilter;

  let selectedFilters: SearchFilter;

  const dispatch = createEventDispatcher<{
    filterSelected: SearchFilter;
  }>();

  const getFilterOptions = (filterName: string): string[] | void => {
    const value = searchFilters[filterName];
    if (!value) {
      return;
    }

    return value;
  };

  const mapToSelectOption = (filters: string[]): SelectOption[] =>
    filters.map((item) => ({
      label: item,
      value: item,
    }));

  const mapTagToOption = (tags: Tag[]): SelectOption[] => {
    return tags.map((item) => ({
      label: item.name,
      value: item.id,
    }));
  };

  $: searchFiltersKeys = Object.keys(searchFilters);

  const handleSelectFilter = (
    filterKey: string,
    e: CustomEvent<SelectOption | null>
  ) => {
    const value = e.detail?.value;

    const newFilter: Partial<SearchFilter> = {
      [filterKey]: value ? [value] : null,
    };

    selectedFilters = mergeSearchFilters(selectedFilters, newFilter);

    dispatch("filterSelected", selectedFilters);
  };
</script>

<h6>{sectionTitle}</h6>

{#each searchFiltersKeys as filterName}
  {@const options = getFilterOptions(filterName)}
  {#if options}
    <div class="fr-mb-2w">
      <p>{DATASET_FILTERS_TRANSLATION[filterName]}</p>
      <SearchableSelect
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter(filterName, e)}
        options={mapToSelectOption(options)}
      />
    </div>
  {/if}
{/each}

<style>
  p {
    padding: 0;
  }
</style>
