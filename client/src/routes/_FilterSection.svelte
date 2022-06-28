<script lang="ts">
  import { DATASET_FILTERS_TRANSLATION } from "src/constants";

  import type { SelectOption } from "src/definitions/form";
  import type { SelectableSearchFilter } from "src/definitions/datasets";

  import SearchableSelect from "src/lib/components/SearchableSelect/SearchableSelect.svelte";
  import { createEventDispatcher } from "svelte";
  import { mergeSelectableSearchFilter } from "src/lib/util/dataset";

  export let sectionTitle: string;
  export let searchFilters: SelectableSearchFilter;

  let selectedFilters: Partial<SelectableSearchFilter>;

  const dispatch = createEventDispatcher<{
    filterSelected: Partial<SelectableSearchFilter>;
  }>();

  $: searchFiltersKeys = Object.keys(searchFilters);

  const handleSelectFilter = (
    filterKey: string,
    e: CustomEvent<SelectOption | null>
  ) => {
    const value = e.detail;

    const newFilter: Partial<SelectableSearchFilter> = {
      [filterKey]: value ? [value] : null,
    };

    if (selectedFilters) {
      selectedFilters = mergeSelectableSearchFilter(selectedFilters, newFilter);
    } else {
      selectedFilters = newFilter;
    }

    dispatch("filterSelected", selectedFilters);
  };
</script>

<h6>{sectionTitle}</h6>

{#each searchFiltersKeys as filterName}
  {@const options = searchFilters[filterName]}
  {#if options}
    <div class="fr-mb-2w">
      <SearchableSelect
        label={DATASET_FILTERS_TRANSLATION[filterName]}
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter(filterName, e)}
        {options}
      />
    </div>
  {/if}
{/each}

<style>
  p {
    padding: 0;
  }
</style>
