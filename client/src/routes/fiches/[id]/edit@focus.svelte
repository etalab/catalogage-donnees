<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { getDatasetByID, updateDataset } from "$lib/repositories/datasets";

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
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import type { Dataset, DatasetFormData } from "src/definitions/datasets";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import paths from "$lib/paths";
  import { isAdmin, user } from "$lib/stores/auth";
  import { deleteDataset } from "$lib/repositories/datasets";

  export let dataset: Dataset;

  let segment = "";

  const id = $page.params.id;
  let loading = false;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      await updateDataset({ fetch, id, data: event.detail });
      await goto(paths.datasetDetail({ id }));
    } finally {
      loading = false;
    }
  };

  const onClickDelete = async (): Promise<void> => {
    const confirmed = confirm(
      "Voulez-vous vraiment supprimer ce jeu de données ? Cette opération est irréversible."
    );

    if (!confirmed) {
      return;
    }

    await deleteDataset({ fetch, apiToken: $user.apiToken, id: dataset.id });
    await goto(paths.home);
  };
</script>

<header class="fr-m-4w">
  <h5>Modifier le jeu de donnée</h5>
</header>

<section class="fr-container">
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-lg-3">
      <nav class="fr-sidemenu fr-sidemenu--sticky" aria-label="Menu latéral">
        <div class="fr-sidemenu__inner">
          <button
            class="fr-sidemenu__btn"
            hidden
            aria-controls="fr-sidemenu-wrapper"
            aria-expanded="false">Dans cette rubrique</button
          >
          <div class="fr-collapse" id="fr-sidemenu-wrapper">
            <ul class="fr-sidemenu__list">
              <li class="fr-sidemenu__item">
                <a
                  on:click={() => (segment = "information-generales")}
                  aria-current={segment === "information-generales"
                    ? "page"
                    : undefined}
                  class="fr-sidemenu__link"
                  href="#information-generales"
                  target="_self">Informations générales</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  on:click={() => (segment = "source-formats")}
                  aria-current={segment === "source-formats"
                    ? "page"
                    : undefined}
                  class="fr-sidemenu__link"
                  href="#source-formats"
                  target="_self">Sources et formats</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  on:click={() => (segment = "contacts")}
                  aria-current={segment === "contacts" ? "page" : undefined}
                  class="fr-sidemenu__link"
                  href="#contacts"
                  target="_self">Contacts</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  on:click={() => (segment = "mise-a-jour")}
                  aria-current={segment === "mise-a-jour" ? "page" : undefined}
                  class="fr-sidemenu__link"
                  href="#mise-a-jour"
                  target="_self">Mise à jour</a
                >
              </li>
              <li class="fr-sidemenu__item">
                <a
                  on:click={() => (segment = "ouverture")}
                  aria-current={segment === "ouverture" ? "page" : undefined}
                  class="fr-sidemenu__link"
                  href="#ouverture"
                  target="_self">Ouverture</a
                >
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
    <div class="fr-col-lg-9">
      <DatasetForm
        initial={dataset}
        {loading}
        submitLabel="Modifier ce jeu de données"
        loadingLabel="Modification en cours..."
        on:save={onSave}
      />

      {#if $isAdmin}
        <div class="fr-alert fr-alert--error fr-mt-8w">
          <p>
            <strong> Zone de danger </strong>
            <em>(visible car vous avez le rôle admin)</em>
          </p>

          <button
            class="fr-btn fr-btn--secondary"
            on:click|preventDefault={onClickDelete}
          >
            Supprimer ce jeu de données
          </button>
        </div>
      {/if}
    </div>
  </div>
</section>
