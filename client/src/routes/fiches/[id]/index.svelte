<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasetByID } from "$lib/repositories/datasets";
  import { apiToken } from "$lib/stores/auth";

  export const load: Load = async ({ fetch, params }) => {
    const dataset = await getDatasetByID({
      fetch,
      apiToken: get(apiToken),
      id: params.id,
    });

    return {
      props: {
        dataset,
      },
    };
  };
</script>

<script lang="ts">
  import paths from "$lib/paths";
  import {
    GEOGRAPHICAL_COVERAGE_LABELS,
    UPDATE_FREQUENCY_LABELS,
  } from "src/constants";
  import type { Dataset } from "src/definitions/datasets";
  import { formatFullDate, splitParagraphs } from "src/lib/util/format";
  import { Maybe } from "$lib/util/maybe";

  export let dataset: Maybe<Dataset>;

  const editUrl = Maybe.map(dataset, (dataset) =>
    paths.datasetEdit({ id: dataset.id })
  );
</script>

{#if Maybe.Some(dataset) && Maybe.Some(editUrl)}
  <div class="fr-container fr-mb-5w">
    <section class="header">
      <div class="header-headlines">
        <p class="fr-logo" title="république française">
          {@html "Ministère<br />de la culture"}
        </p>
        <div>
          <p class="fr-m-0 fr-text-mention--grey">
            {dataset.service}
          </p>
          <h1 class="fr-mb-0">
            {dataset.title}
          </h1>
        </div>
      </div>

      <ul
        class="header-toolbar fr-grid-row fr-btns-group fr-btns-group--inline fr-btns-group--icon-right fr-my-5w"
      >
        <li>
          <a
            href={editUrl}
            class="fr-btn fr-btn--secondary fr-fi-edit-fill"
            title="Modifier ce jeu de données"
          >
            Modifier
          </a>
        </li>
        <li>
          <a
            class="fr-btn fr-btn--secondary fr-fi-mail-line"
            title="Contacter le producter du jeu de données par email"
            href="mailto:{dataset.entrypointEmail}"
          >
            Contacter le producteur
          </a>
        </li>
      </ul>
    </section>

    <section class="layout">
      <aside
        aria-label="Métadonnées sur ce jeu de données"
        class="fr-container"
      >
        <h6 class="fr-mb-2w">Informations générales</h6>

        <div class="aside-entry">
          <span class="fr-fi--lg fr-fi-x-bank-line" aria-hidden="true" />
          <p>
            <span class="fr-text--xs">Producteur</span><br />
            <span>{dataset.service}</span>
          </p>
        </div>
        <div class="aside-entry">
          <span class="fr-fi--lg fr-fi-x-map-2-line" aria-hidden="true" />
          <p>
            <span class="fr-text--xs">Couverture géographique</span><br />
            <span>
              {GEOGRAPHICAL_COVERAGE_LABELS[dataset.geographicalCoverage]}
            </span>
          </p>
        </div>

        <h6 class="fr-mt-4w fr-mb-2w">Mise à jour</h6>

        <div class="aside-entry">
          <span
            class="fr-fi--lg fr-fi-x-calendar-check-line"
            aria-hidden="true"
          />
          <p>
            <span class="fr-text--xs">Date de dernière mise à jour</span><br />
            <span
              >{dataset.lastUpdatedAt
                ? formatFullDate(dataset.lastUpdatedAt)
                : "-"}</span
            >
          </p>
        </div>
        <div class="aside-entry">
          <span class="fr-fi--lg fr-fi-refresh-line" aria-hidden="true" />
          <p>
            <span class="fr-text--xs">Fréquence de mise à jour</span><br />
            <span
              >{dataset.updateFrequency
                ? UPDATE_FREQUENCY_LABELS[dataset.updateFrequency]
                : "-"}</span
            >
          </p>
        </div>
      </aside>

      <div
        class="fr-text--sm"
        aria-label="Description du jeu de données"
        data-testid="dataset-description"
      >
        {#each splitParagraphs(dataset.description) as text}
          <p class="fr-text--lg">
            {text}
          </p>
        {/each}
      </div>
    </section>
  </div>
{/if}

<style>
  .header {
    margin-top: 1.5rem;
  }

  @media (min-width: 36em /* sm */) {
    .header-headlines {
      display: grid;
      grid-template-columns: auto 1fr;
      column-gap: 1em;
      align-items: center;
    }
  }

  @media (min-width: 48em /* md */) {
    .header-headlines {
      column-gap: 3em;
    }

    .layout {
      display: grid;
      grid-template-columns: auto 1fr;
      column-gap: 3rem;
    }

    .header-toolbar {
      justify-content: flex-end;
    }
  }

  .aside-entry {
    align-items: center;
    display: flex;
    gap: 10px;
    margin-bottom: 1rem;
  }

  .aside-entry [class*="fr-fi"] {
    color: var(--text-action-high-blue-france);
    display: inline-block;
    height: 32px;
    width: 32px;
  }

  .aside-entry p {
    margin-bottom: 0;
  }
</style>
