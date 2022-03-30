<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { getDatasetByID } from "$lib/repositories/datasets";

  export const load: Load = async ({ fetch, params }) => {
    const dataset = await getDatasetByID({ fetch, id: params.id });
    return {
      props: {
        dataset,
      },
    };
  };
</script>

<script lang="ts">
  import paths from "$lib/paths";
  import type { Dataset } from "src/definitions/datasets";

  export let dataset: Dataset;

  const editUrl = paths.datasetEdit({ id: dataset.id });
</script>

<section class="fr-container header">
  <div class="header-headlines">
    <p class="fr-logo" title="république française">
      {@html "Ministère<br />de la culture"}
    </p>
    <div>
      <p class="fr-m-0 fr-text-mention--grey">Ministère de la culture</p>
      <h1>
        {dataset.title}
      </h1>
    </div>
  </div>

  <ul
    class="header-toolbar fr-grid-row fr-btns-group fr-btns-group--inline fr-btns-group--icon-right fr-mb-3w"
  >
    <li>
      <a
        href={editUrl}
        class="fr-btn fr-btn--secondary fr-fi-edit-fill"
        title="Proposer une modification pour cette fiche de données"
      >
        Proposer une modification
      </a>
    </li>
    <li>
      <a
        class="fr-btn fr-btn--secondary fr-fi-mail-fill"
        title="Contacter le producter du jeu de données par email"
        href="mailto:{dataset.entrypointEmail}"
      >
        Contacter le producteur
      </a>
    </li>
    <li>
      <button
        class="fr-btn fr-btn--secondary fr-fi-x-heart-line"
        title="Recevoir des alertes lors d'une modification à cette fiche de données"
      >
        Suivre
      </button>
    </li>
  </ul>
</section>

<section class="layout fr-container">
  <aside
    role="contentinfo"
    aria-label="Métadonnées sur ce jeu de données"
    class="fr-container"
  >
    <div class="aside-entry">
      <span class="fr-fi--lg fr-fi-x-bank-line" aria-hidden="true" />
      <p>
        <span class="fr-text--xs">Producteur</span><br />
        <span>DRAC Bretagne</span>
      </p>
    </div>
    <div class="aside-entry">
      <span class="fr-fi--lg fr-fi-x-map-2-line" aria-hidden="true" />
      <p>
        <span class="fr-text--xs">Couverture géographique</span><br />
        <span>France métropolitaine</span>
      </p>
    </div>
    <div class="aside-entry">
      <span class="fr-fi--lg fr-fi-calendar-line" aria-hidden="true" />
      <p>
        <span class="fr-text--xs">Couverture temporelle</span><br />
        <span>2015-2022</span>
      </p>
    </div>

    <h6>Temporalité</h6>

    <div class="aside-entry">
      <span class="fr-fi--lg fr-fi-x-calendar-check-line" aria-hidden="true" />
      <p>
        <span class="fr-text--xs">Date de dernière mise à jour</span><br />
        <span>13 septembre 2021</span>
      </p>
    </div>
    <div class="aside-entry">
      <span class="fr-fi--lg fr-fi-refresh-line" aria-hidden="true" />
      <p>
        <span class="fr-text--xs">Fréquence de mise à jour</span><br />
        <span>Mensuelle ou plusieurs fois par an</span>
      </p>
    </div>
    <div class="aside-entry">
      <span class="fr-fi--lg fr-fi-x-cake-2-line" aria-hidden="true" />
      <p>
        <span class="fr-text--xs">Date de première publication</span><br />
        <span>15 décembre 2019</span>
      </p>
    </div>
  </aside>

  <section>
    <div class="fr-tabs">
      <ul
        class="fr-tabs__list"
        role="tablist"
        aria-label="Onglets de navigation dans la fiche de données"
      >
        <li role="presentation">
          <button
            id="tabpanel-resume"
            class="fr-tabs__tab"
            tabindex="0"
            role="tab"
            aria-selected="true"
            aria-controls="tabpanel-resume-panel"
          >
            Résumé
          </button>
        </li>
        <li role="presentation">
          <button
            id="tabpanel-sources"
            class="fr-tabs__tab"
            tabindex="-1"
            role="tab"
            aria-selected="false"
            aria-controls="tabpanel-sources-panel"
          >
            Sources
          </button>
        </li>
        <li role="presentation">
          <button
            id="tabpanel-contenu"
            class="fr-tabs__tab"
            tabindex="-1"
            role="tab"
            aria-selected="false"
            aria-controls="tabpanel-contenu-panel"
          >
            Contenu
          </button>
        </li>
        <li role="presentation">
          <button
            id="tabpanel-discussions"
            class="fr-tabs__tab"
            tabindex="-1"
            role="tab"
            aria-selected="false"
            aria-controls="tabpanel-discussions-panel"
          >
            Discussion
          </button>
        </li>
      </ul>

      <div
        id="tabpanel-resume-panel"
        class="fr-tabs__panel fr-tabs__panel--selected"
        role="tabpanel"
        aria-labelledby="tabpanel-resume"
        tabindex="0"
      >
        {dataset.description}
      </div>

      <div
        id="tabpanel-sources-panel"
        class="fr-tabs__panel"
        role="tabpanel"
        aria-labelledby="tabpanel-sources"
        tabindex="0"
      >
        À venir
      </div>

      <div
        id="tabpanel-contenu-panel"
        class="fr-tabs__panel"
        role="tabpanel"
        aria-labelledby="tabpanel-contenu"
        tabindex="0"
      >
        À venir
      </div>

      <div
        id="tabpanel-discussions-panel"
        class="fr-tabs__panel"
        role="tabpanel"
        aria-labelledby="tabpanel-discussions"
        tabindex="0"
      >
        À venir
      </div>
    </div>
  </section>
</section>

<style>
  .header {
    margin-top: 1.5rem;
  }

  @media (min-width: 36em /* sm */) {
    .header {
      margin-top: 3rem;
    }

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
      column-gap: 1em;
    }

    .header-toolbar {
      justify-content: flex-end;
    }
  }

  .aside-entry {
    align-items: center;
    display: flex;
    gap: 10px;
    margin-bottom: 2em;
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
