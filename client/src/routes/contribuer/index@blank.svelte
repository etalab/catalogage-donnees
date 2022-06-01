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

  import Modal from "src/lib/components/Modal/Modal.svelte";

  let modalTriggerId = "confirm-stop-contributing-modal";

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
</script>

<header class="fr-p-4w">
  <h5>Créer une fiche de jeu de données</h5>
  <button
    class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
    data-fr-opened="false"
    aria-controls={formHasBeenTouched ? modalTriggerId : undefined}
    on:click={() => {
      if (!formHasBeenTouched) {
        window.history.back();
      }
    }}
  >
    {""}
  </button>
</header>

<Modal triggerId={modalTriggerId} />

{#if Maybe.Some(tags)}
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
