<script lang="ts">
  import type { SelectOption } from "src/definitions/form";
  import type { SearchFilter } from "src/definitions/searchFilters";

  import SearchableSelect from "src/lib/components/SearchableSelect/SearchableSelect.svelte";

  export let sectionTitle: string;
  export let searchFilters: SearchFilter;

  const getFilterOptions = (filterName: string): string[] => {
    return searchFilters[filterName];
  };

  const mapToSelectOption = (filters: string[]): SelectOption[] =>
    filters.map((item) => ({
      label: item,
      value: item,
    }));

  $: searchFiltersKeys = Object.keys(searchFilters);

  let selectedFilters: string[] = [];

  const handleSelectFilter = (e: CustomEvent<SelectOption | null>) => {
    if (e.detail) {
      selectedFilters = [...selectedFilters, e.detail?.value];
    }
  };

  const titleMappingTable = {
    geographical_coverage: "Couverture géographique",
    service: "Service producteur de la donnée",
    formats: "Formats de mise à disposition",
    technical_source: "Système d’information source",
    tags: "Mots-clés",
  };
</script>

<h6>{sectionTitle}</h6>

{#each searchFiltersKeys as key}
  <div class="fr-mb-2w">
    <p>{titleMappingTable[key]}</p>
    <SearchableSelect
      buttonPlaceholder="Rechercher ..."
      inputPlaceholder="Rechercher ..."
      on:clickItem={handleSelectFilter}
      options={mapToSelectOption(getFilterOptions(key))}
    />
  </div>
{/each}

<style>
  p {
    padding: 0;
  }
</style>
