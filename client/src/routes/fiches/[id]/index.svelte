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

  const editUrl = paths.datasetEdit({ id : dataset.id});
</script>

<section class="fr-container fr-mt-9w">
  <div class="fr-grid-row fr-grid-row--middle fr-mb-3w">
    <div class="fr-col-2">
      <p class="fr-logo" title="république française">
        {@html "Ministère<br />de la culture"}
      </p>
    </div>
    <div class="fr-col">
      <p class="fr-mb-0 fr-text-mention--grey">Ministère de la culture</p>
      <h1>
        {dataset.title}
      </h1>
    </div>
  </div>

  <ul
    class="fr-grid-row fr-grid-row--right fr-btns-group fr-btns-group--inline fr-btns-group--icon-right"
  >
    <li>
      <a
        href={editUrl}
        class="fr-btn fr-btn--secondary fr-fi-edit-fill fr-icon-edit-fill"
        title="Proposer une modification pour cette fiche de données"
      >
        Proposer une modification
      </a>
    </li>
    <li>
      <button
        class="fr-btn fr-btn--secondary fr-fi-mail-fill fr-icon-mail-fill"
        title="Contacter le producter du jeu de données"
      >
        Contacter le producteur
      </button>
    </li>
    <li>
      <button
        class="fr-btn fr-btn--secondary fr-fi-eye-fill fr-icon-eye-fill"
        title="Recevoir des alertes lors d'une modification à cette fiche de données"
      >
        Suivre
      </button>
    </li>
  </ul>
</section>

<section class="fr-container">
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-4">
      <p>Producteur : DRAC Bretagne</p>
      <p>Couverture géographique : France métropolitaine</p>
    </div>
    <div class="fr-col fr-tabs">
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
            Discussion (9)
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
        <p>
          <strong> Propos liminaires </strong>
        </p>
        <p>
          Conformément au décret n° AAAA-BBBB du DD mm YYYY relatif à la
          publication de...
        </p>
      </div>

      <div
        id="tabpanel-sources-panel"
        class="fr-tabs__panel"
        role="tabpanel"
        aria-labelledby="tabpanel-sources"
        tabindex="0"
      >
        Sources !
      </div>

      <div
        id="tabpanel-contenu-panel"
        class="fr-tabs__panel"
        role="tabpanel"
        aria-labelledby="tabpanel-contenu"
        tabindex="0"
      >
        Contenu !
      </div>

      <div
        id="tabpanel-discussions-panel"
        class="fr-tabs__panel"
        role="tabpanel"
        aria-labelledby="tabpanel-discussions"
        tabindex="0"
      >
        Discussions !
      </div>
    </div>
  </div>
</section>
