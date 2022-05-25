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
  import AsideItem from "./_AsideItem.svelte";

  export let dataset: Maybe<Dataset>;

  const editUrl = Maybe.map(dataset, (dataset) =>
    paths.datasetEdit({ id: dataset.id })
  );
</script>

<section class="fr-container">
  {#if Maybe.Some(dataset) && Maybe.Some(editUrl)}
    <header class="fr-grid-row">
      <section class="fr-col-12 fr-mt-5w">
        <div class="header-headlines">
          <p class="fr-logo" title="république française">
            {@html "Ministère<br />de la culture"}
          </p>
          <div>
            <p class="fr-m-0 fr-text-mention--grey">Ministère de la culture</p>
            <h1 class="fr-mb-0">
              {dataset.title}
            </h1>
            <div class="header-headlines-tags fr-mt-2w">
              {#each dataset.tags as tag}
                <span class="fr-badge fr-badge--info fr-badge--no-icon">
                  {tag.name}</span
                >
              {/each}
            </div>
          </div>
        </div>

        <ul
          class="header-toolbar fr-btns-group fr-btns-group--inline fr-btns-group--icon-right fr-my-5w"
        >
          <li>
            <a
              href={editUrl}
              class="fr-btn fr-btn--secondary fr-icon-edit-fill"
              title="Modifier ce jeu de données"
            >
              Modifier
            </a>
          </li>
          <li>
            <a
              class="fr-btn fr-btn--secondary fr-icon-mail-line"
              title="Contacter le producter du jeu de données par email"
              href="mailto:{dataset.producerEmail}"
            >
              Contacter le producteur
            </a>
          </li>
        </ul>
      </section>
    </header>

    <div class="fr-grid-row fr-grid-row--gutters">
      <aside class="fr-col-4">
        <h6 class="fr-mb-2w">Ouverture</h6>

        <AsideItem
          icon="fr-icon-x-open-data"
          label="Accessibilité aux données"
          value={dataset.publishedUrl ? "Ouverte" : "Restreinte"}
        />
        {#if dataset.publishedUrl}
          <a
            class="fr-btn fr-btn--icon-right fr-icon-external-link-line"
            href={dataset.publishedUrl}
            target="_blank"
          >
            Voir les données
          </a>
        {:else}
          <p class="fr-text--xs fr-text-mention--grey fr-mb-0">
            Veuillez prendre contact avec le producteur afin d'obtenir l'accès
            au jeu de données.
          </p>
        {/if}

        <h6 class="fr-mt-4w fr-mb-2w">Informations générales</h6>

        <AsideItem
          icon="fr-icon-bank-line"
          label="Producteur"
          value={dataset.service}
        />

        <AsideItem
          icon="fr-icon-x-map-2-line"
          label="Couverture géographique"
          value={GEOGRAPHICAL_COVERAGE_LABELS[dataset.geographicalCoverage]}
        />

        <h6 class="fr-mt-4w fr-mb-2w">Mise à jour</h6>

        <AsideItem
          icon="fr-icon-x-calendar-check-line"
          label="Date de dernière mise à jour"
          value={Maybe.map(dataset.lastUpdatedAt, (v) => formatFullDate(v))}
        />

        <AsideItem
          icon="fr-icon-refresh-line"
          label="Fréquence de mise à jour"
          value={Maybe.map(
            dataset.updateFrequency,
            (v) => UPDATE_FREQUENCY_LABELS[v]
          )}
        />
      </aside>

      <section
        class="fr-col-8 fr-text--sm"
        aria-label="Description du jeu de données"
        data-testid="dataset-description"
      >
        {#each splitParagraphs(dataset.description) as text}
          <p class="fr-text--lg">
            {text}
          </p>
        {/each}
      </section>
    </div>
  {/if}
</section>

<style>
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

    .header-toolbar {
      justify-content: flex-end;
    }
  }

  .header-headlines-tags {
    display: flex;
    gap: 10px;
  }
</style>
