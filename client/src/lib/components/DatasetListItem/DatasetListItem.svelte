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

<li class="fr-p-3w">
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
      Bibliothèque nationale de France
    </p>
    <div class="metadata-items">
      <span> France </span>
      <span> 2010-2018 </span>
      <span> {formatFormats(dataset)} </span>
      <span> Qualité : haute </span>
      <span> Open data </span>
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
    <p class="fr-mb-2w fr-text--sm fr-text-mention--grey">
      {capitalize(
        formatDaysMonthsOrYearsToNow(dataset.catalogRecord.createdAt)
      )}
    </p>
    <a
      href={paths.datasetDetail({ id: dataset.id })}
      class="fr-link fr-fi-arrow-right-line fr-link--icon-right"
      title="Consulter cette fiche de données"
    >
      Voir
    </a>
  </div>
</li>

<style>
  li {
    display: grid;
    grid-template-columns: auto 1fr auto;
    column-gap: 1em;
  }

  li:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }

  .metadata-items {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -1em;
  }

  .metadata-items > * {
    flex: 1 1 auto;
    margin: 0 1em;
  }

  .actions {
    text-align: right;
  }
</style>
