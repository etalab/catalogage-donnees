<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import {
    DATA_FORMAT_SHORT_NAMES,
    GEOGRAPHICAL_COVERAGE_LABELS,
  } from "src/constants";
  import paths from "$lib/paths";
  import { capitalize, formatDaysMonthsOrYearsToNow } from "$lib/util/format";

  export let dataset: Dataset;

  const formatFormats = (dataset: Dataset) => {
    return dataset.formats
      .map((format) => DATA_FORMAT_SHORT_NAMES[format])
      .join(", ");
  };
</script>

<li class="fr-p-3w container">
  <a
    href={paths.datasetDetail({ id: dataset.id })}
    title="Consulter cette fiche de données"
  >
    <p class="fr-logo fr-logo--sm fr-p-0" title="république française">
      {@html "Ministère<br />de la culture"}
    </p>

    <div class="fr-container">
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

      <p class="fr-m-0 fr-text--sm fr-text-mention--grey">
        {dataset.service}
      </p>

      <div class="metadata-items fr-mt-1w">
        <div>
          <span class="fr-fi fr-fi-x-map-2-line" aria-hidden="true" />
          <p class="fr-text--xs fr-my-0">
            <span class="fr-text-mention--grey">Couverture géographique</span>
            <br />
            <span
              >{GEOGRAPHICAL_COVERAGE_LABELS[
                dataset.geographicalCoverage
              ]}</span
            >
          </p>
        </div>
        <div>
          <span class="fr-fi fr-fi-file-line" aria-hidden="true" />
          <p class="fr-text--xs fr-my-0">
            <span class="fr-text-mention--grey">Formats</span> <br />
            <span>{formatFormats(dataset)}</span>
          </p>
        </div>
      </div>
      {#if dataset.headlines}
        <p class="fr-mb-0 fr-mt-1w fr-text--sm fr-text-mention--grey">
          <em data-testid="headlines-description"
            >... {@html dataset.headlines.description} ...</em
          >
        </p>
      {/if}
    </div>

    <div class="actions">
      <p class="fr-mb-2w fr-text--sm">
        {capitalize(
          formatDaysMonthsOrYearsToNow(dataset.catalogRecord.createdAt)
        )}
      </p>

      <span> Voir </span>
    </div>
  </a>
</li>

<style>
  a {
    display: flex;
    width: 100%;
  }
  li:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }

  .metadata-items {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -2em;
  }

  .metadata-items > * {
    flex: 0 1 auto;
    margin: 0 2em;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    column-gap: 0.5rem;
  }

  .metadata-items [class*="fr-fi"] {
    color: var(--text-action-high-blue-france);
    display: inline-block;
  }

  .actions {
    text-align: right;
  }
  [href] {
    box-shadow: none;
  }
</style>
