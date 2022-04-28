<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";
  let segment = "";
  let loading = false;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      const dataset = await createDataset({ fetch, data: event.detail });
      await goto(paths.datasetDetail({ id: dataset.id }));
    } finally {
      loading = false;
    }
  };
</script>

<svelte:head>
  <title>Contribuer</title>
</svelte:head>

<header class="fr-m-4w">
  <h5>Contribuer un jeu de données</h5>
</header>

<div class="fr-container">
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
      <DatasetForm {loading} on:save={onSave} />
    </div>
  </div>
</div>
