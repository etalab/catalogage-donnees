<script lang="ts">
  import type { Dataset } from "src/definitions/datasets";

  export let datasets: Dataset[];
</script>

<ul>
  {#each datasets as dataset, index (dataset.id)}
    {@const lastChild = index === datasets.length - 1}
    <li class="fr-pb-2w">
      <div class="fr-container">
        <div class="fr-grid-row">
          <div class="fr-col-2">
            <p class="fr-text--sm">Ministère de la culture</p>
          </div>
          <div class="fr-col">
            <div class="fr-container">
              <p class="fr-grid-row">
                <strong>
                  {dataset.title}
                </strong>
              </p>
              <p class="fr-grid-row fr-text--sm fr-text-mention--grey">
                Bibliothèque nationale de France
              </p>
              <div class="fr-grid-row">
                <span class="fr-col"> France </span>
                <span class="fr-col"> 2010-2018 </span>
                <span class="fr-col"> CSV, API, BDD </span>
                <span class="fr-col"> Qualité : haute </span>
                <span class="fr-col"> Open data </span>
              </div>
            </div>
          </div>
          <div class="fr-col-2 fr-container fr-container--fluid">
            <div class="fr-grid-row fr-grid-row--right">
              <p class="fr-text--sm fr-text-mention--grey">Il y a 3 jours</p>
              <a
                href={`/fiches/${dataset.id}`}
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
    {#if !lastChild}
      <hr />
    {/if}
  {/each}
</ul>

<style>
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
</style>
