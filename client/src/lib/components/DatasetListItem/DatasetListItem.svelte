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

<li>
  <a
    data-test-id="dataset-list-item"
    class="fr-p-2w"
    href={paths.datasetDetail({ id: dataset.id })}
    title="Consulter cette fiche de données"
  >
    <div class="logo">
      <p class="fr-logo fr-logo--sm fr-p-0" title="république française">
        {@html "Ministère<br />de la culture"}
      </p>
    </div>

    <div class="meta-data fr-px-2w">
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

        <p class="fr-m-0 fr-text--sm fr-text-mention--grey">
          {dataset.service}
        </p>
      </div>

      <div class="meta-data-coverage-format">
        <div class="metadata-items fr-mt-1w">
          <div>
            <span class="fr-fi fr-fi-x-map-2-line" aria-hidden="true" />
            <p class="fr-text--xs fr-my-0 fr-px-1w">
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
            <p class="fr-text--xs fr-my-0 fr-px-1w">
              <span class="fr-text-mention--grey">Formats</span> <br />
              <span>{formatFormats(dataset)}</span>
            </p>
          </div>
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

    <div class="opening">
      {#if dataset.publishedUrl}
        <div class="opening__open-data-status">
          <span class="fr-fi-x-open-data fr-text-label--blue-france" />
          <p class="fr-text--xs fr-my-0 fr-px-1w">
            <span class="fr-text-mention--grey">Ouverture</span>
            <br />
            <span>Open data</span>
          </p>
        </div>
      {:else}
        <div class="opening__open-data-status">
          <span class="fr-fi-x-open-data fr-text-label--blue-france" />
          <p class="fr-text--xs fr-my-0 fr-px-1w">
            <span class="fr-text-mention--grey">Ouverture</span>
            <br />
            <span>Restreint</span>
          </p>
        </div>
      {/if}
    </div>

    <div class="action">
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
  li,
  a[data-test-id="dataset-list-item"] {
    width: 100%;
  }

  a[data-test-id="dataset-list-item"] {
    display: flex;
    width: 100%;
    height: 100%;
  }

  a[data-test-id="dataset-list-item"]:hover {
    --a: 0.3;
    --blend-size: 100%;
  }

  .logo {
    width: 10%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .meta-data {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .meta-data-coverage-format {
    max-width: 65%;
  }

  .opening {
    display: flex;
    align-items: flex-end;
    width: 20%;
  }

  .opening__open-data-status {
    padding: 5px;
    display: flex;
    align-items: center;
  }

  .action {
    width: 10%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
  }

  li:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }

  .metadata-items {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    margin: 0 -2em;
  }

  .metadata-items > * {
    margin: 0 2em;
    display: flex;
  }

  .metadata-items [class*="fr-fi"] {
    color: var(--text-action-high-blue-france);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 0.5rem;
  }

  [href] {
    box-shadow: none;
  }
</style>
