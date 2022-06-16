<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  export const prerender = true;
  import { getTags } from "src/lib/repositories/tags";
  import { apiToken } from "$lib/stores/auth";
  import { get } from "svelte/store";
  export const load: Load = async ({ fetch }) => {
    const tags = await getTags({
      fetch,
      apiToken: get(apiToken),
    });
    return {
      props: {
        tags,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";

  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";
  import { Maybe } from "$lib/util/maybe";
  import DatasetFormLayout from "src/lib/components/DatasetFormLayout/DatasetFormLayout.svelte";
  import type { Tag } from "src/definitions/tag";
  import ModalExitFormConfirmation from "src/lib/components/ModalExitFormConfirmation/ModalExitFormConfirmation.svelte";

  let modalControlId = "confirm-stop-contributing-modal";

  let loading = false;

  let formHasBeenTouched = false;

  export let tags: Maybe<Tag[]>;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      const tagIds = event.detail.tags.map((item) => item.id);
      const dataset = await createDataset({
        fetch,
        apiToken: $apiToken,
        data: { tagIds, ...event.detail },
      });

      if (Maybe.Some(dataset)) {
        await goto(paths.datasetDetail({ id: dataset.id }));
      }
    } finally {
      loading = false;
    }
  };

  const handleExitForm = () => {
    history.go(-1);
  };
</script>

<header class="fr-p-4w">
  <h5>Créer une fiche de jeu de données</h5>

  {#if formHasBeenTouched}
    <button
      class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
      data-fr-opened="false"
      data-testid="exit-contribution-form"
      aria-controls={modalControlId}
    >
      {""}
    </button>
  {:else}
    <button
      data-testid="exit-contribution-form"
      class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
      on:click={handleExitForm}
    >
      {""}
    </button>
  {/if}
</header>

{#if Maybe.Some(tags)}
  <ModalExitFormConfirmation
    on:confirm={handleExitForm}
    controlId={modalControlId}
  />

  <DatasetFormLayout>
    <DatasetForm
      {tags}
      {loading}
      on:save={onSave}
      on:touched={() => (formHasBeenTouched = true)}
    />
  </DatasetFormLayout>
{/if}

<style>
  header {
    height: 10vh;
    display: flex;
    position: sticky;
    justify-content: space-between;
    top: 0;
    z-index: 55;
    background-color: var(--background-default-grey);
  }
</style>
