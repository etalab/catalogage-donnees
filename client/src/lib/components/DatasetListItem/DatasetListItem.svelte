<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";
  import { DATA_FORMAT_SHORT_NAMES } from "src/constants";
  import paths from "$lib/paths";
  import { capitalize, formatDaysMonthsOrYearsToNow } from "$lib/util/format";

  export let dataset: Dataset;

  const formatFormats = (dataset: Dataset) => {
    return dataset.formats
      .map((format) => DATA_FORMAT_SHORT_NAMES[format])
      .join(", ");
  };
</script>

<li class="fr-p-2w">
  <div class="fr-container">
    <div class="fr-grid-row">
      <div class="fr-col-2">
        <p class="fr-text--sm">Ministère de la culture</p>
      </div>
      <div class="fr-col">
        <div class="fr-container">
          <p class="fr-grid-row">
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
          <p class="fr-grid-row fr-text--sm fr-text-mention--grey">
            Bibliothèque nationale de France
          </p>
          <div class="fr-grid-row">
            <span class="fr-col"> France </span>
            <span class="fr-col"> 2010-2018 </span>
            <span class="fr-col"> {formatFormats(dataset)} </span>
            <span class="fr-col"> Qualité : haute </span>
            <span class="fr-col"> Open data </span>
          </div>
          {#if dataset.headlines}
            <div class="fr-grid-row fr-mt-1w">
              <p class="fr-text--sm fr-text-mention--grey">
                <em data-testid="headlines-description"
                  >... {@html dataset.headlines.description} ...</em
                >
              </p>
            </div>
          {/if}
        </div>
      </div>
      <div class="fr-col-2 fr-container fr-container--fluid">
        <div
          class="fr-grid-row fr-grid-row--right fr-text--sm fr-text-mention--grey dataset-created-at"
        >
          {capitalize(formatDaysMonthsOrYearsToNow(dataset.createdAt))}
        </div>
        <div class="fr-grid-row fr-grid-row--right">
          <a
            href={paths.datasetDetail({ id: dataset.id })}
            class="fr-link fr-fi-arrow-right-line fr-link--icon-right"
            title="Consulter cette fiche de données"
          >
            Voir
          </a>
        </div>
      </div>
    </div>
  </div>
</li>

<style>
  li:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }

  .dataset-created-at {
    text-align: right;
  }
</style>
