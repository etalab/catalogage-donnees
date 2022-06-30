<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import { DATASET_FILTERS_TRANSLATION } from "src/constants";

  import type { SelectOption } from "src/definitions/form";
  import type { SelectableDatasetFilter } from "src/definitions/datasets";
  import { mergeSelectableDatasetFilter } from "$lib/util/dataset";

  import SearchableSelect from "$lib/components/SearchableSelect/SearchableSelect.svelte";

  export let sectionTitle: string;
  export let searchFilters: SelectableDatasetFilter;

  let selectedFilters: Partial<SelectableDatasetFilter>;

  const dispatch = createEventDispatcher<{
    filterSelected: Partial<SelectableDatasetFilter>;
  }>();

  $: searchFiltersKeys = Object.keys(searchFilters);

  const handleSelectFilter = (
    filterKey: string,
    e: CustomEvent<SelectOption | null>
  ) => {
    const value = e.detail;

    const newFilter: Partial<SelectableDatasetFilter> = {
      [filterKey]: value ? [value] : null,
    };

    if (selectedFilters) {
      selectedFilters = mergeSelectableDatasetFilter(
        selectedFilters,
        newFilter
      );
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
