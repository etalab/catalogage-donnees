<script lang="ts">
  import {
    DATASET_FILTERS_TRANSLATION,
    type DatasetFilter,
  } from "src/constants";

  import type {
    DatasetFilters,
    SelectableDatasetFilter,
  } from "src/definitions/datasets";
  import type { SelectOption } from "src/definitions/form";
  import SearchableSelect from "src/lib/components/SearchableSelect/SearchableSelect.svelte";
  import { transformSearchFiltersIntoSelectableDatasetFilters } from "src/lib/transformers/dataset";
  import { mergeSelectableDatasetFilter } from "src/lib/util/dataset";
  import { createEventDispatcher } from "svelte";

  export let filters: DatasetFilters;

  let selectedFilters: Partial<SelectableDatasetFilter>;

  const dispatch = createEventDispatcher<{
    change: Partial<SelectableDatasetFilter>;
  }>();

  $: selectableDataSetFilters =
    transformSearchFiltersIntoSelectableDatasetFilters(filters);

  const handleSelectFilter = (
    filterKey: DatasetFilter,
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

    dispatch("change", selectedFilters);
  };
</script>

<section>
  <h6>Informations Générales</h6>

  {#if selectableDataSetFilters.geographical_coverage}
    <div class="fr-mb-2w">
      <SearchableSelect
        label={DATASET_FILTERS_TRANSLATION.geographical_coverage}
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter("geographical_coverage", e)}
        options={selectableDataSetFilters.geographical_coverage}
      />
    </div>
  {/if}

  {#if selectableDataSetFilters.service}
    <div class="fr-mb-2w">
      <SearchableSelect
        label={DATASET_FILTERS_TRANSLATION.service}
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter("service", e)}
        options={selectableDataSetFilters.service}
      />
    </div>
  {/if}
</section>

<section>
  <h6>Sources et Formats</h6>
  {#if selectableDataSetFilters.format}
    <div class="fr-mb-2w">
      <SearchableSelect
        label={DATASET_FILTERS_TRANSLATION.format}
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter("format", e)}
        options={selectableDataSetFilters.format}
      />
    </div>
  {/if}

  {#if selectableDataSetFilters.technical_source}
    <div class="fr-mb-2w">
      <SearchableSelect
        label={DATASET_FILTERS_TRANSLATION.technical_source}
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter("technical_source", e)}
        options={selectableDataSetFilters.technical_source}
      />
    </div>
  {/if}
</section>

<section>
  <h6>Mots-clés Thématiques</h6>
  {#if selectableDataSetFilters.tag_id}
    <div class="fr-mb-2w">
      <SearchableSelect
        label={DATASET_FILTERS_TRANSLATION.tag_id}
        buttonPlaceholder="Rechercher ..."
        inputPlaceholder="Rechercher ..."
        on:clickItem={(e) => handleSelectFilter("tag_id", e)}
        options={selectableDataSetFilters.tag_id}
      />
    </div>
  {/if}
</section>
