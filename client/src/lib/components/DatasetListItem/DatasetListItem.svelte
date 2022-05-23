<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import {
    DATA_FORMAT_SHORT_NAMES,
    GEOGRAPHICAL_COVERAGE_LABELS,
  } from "src/constants";
  import paths from "$lib/paths";
  import { capitalize, formatDaysMonthsOrYearsToNow } from "$lib/util/format";
  import DatasetPropertyList from "../DatasetPropertyList/DatasetPropertyList.svelte";

  export let dataset: Dataset;

  $: properties = [
    {
      label: "Couverture géographique",
      icon: "fr-fi-x-map-2-line",
      value: GEOGRAPHICAL_COVERAGE_LABELS[dataset.geographicalCoverage],
    },
    {
      label: "Formats",
      icon: "fr-fi-file-line",
      value: dataset.formats
        .map((format) => DATA_FORMAT_SHORT_NAMES[format])
        .join(", "),
    },
    {
      label: "Ouverture",
      icon: dataset.publishedUrl
        ? "fr-fi-x-open-data"
        : "fr-fi-x-restricted-data",
      value: dataset.publishedUrl ? "Open data" : "Restreint",
    },
  ];
</script>

<li>
  <a
    data-test-id="dataset-list-item"
    class="item"
    href={paths.datasetDetail({ id: dataset.id })}
    title="Consulter cette fiche de données"
  >
    <div class="item__logo">
      <p class="fr-logo fr-logo--sm">
        {@html "Ministère<br />de la culture"}
      </p>
    </div>

    <div>
      <p class="fr-m-0">
        {#if dataset.headlines}
          <strong data-testid="headlines-title">
            {@html dataset.headlines.title}
          </strong>
        {:else}
          <strong>
            {dataset.title}
          </strong>
        {/if}
      </p>

      <p class="fr-mb-2w fr-text--sm fr-text-mention--grey">
        {dataset.service}
      </p>

      <DatasetPropertyList {properties} />

      {#if dataset.headlines}
        <p class="fr-mb-0 fr-mt-1w fr-text--sm fr-text-mention--grey">
          <em data-testid="headlines-description"
            >... {@html dataset.headlines.description} ...</em
          >
        </p>
      {/if}
    </div>

    <div class="item__actions">
      <p class="fr-text--sm">
        {capitalize(
          formatDaysMonthsOrYearsToNow(dataset.catalogRecord.createdAt)
        )}
      </p>

      <span class="fr-fi-arrow-right-line fr-text-label--blue-france" />
    </div>
  </a>
</li>

<style>
  .item {
    display: grid;
    column-gap: 1rem;
    grid-template-columns: 1fr 8fr 1fr;
    padding: var(--sp-3w) var(--sp-2w);
  }

  .item[href] {
    box-shadow: none;
  }

  .item:hover {
    --a: 0.3;
    --blend-size: 100%;
  }

  .item__logo {
    display: flex;
    padding-right: var(--sp-1w);
    align-items: center;
  }

  .item__actions {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
  }

  li:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }

  p {
    padding: 0;
    margin: 0;
  }
</style>
