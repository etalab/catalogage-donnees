<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasetByID, updateDataset } from "$lib/repositories/datasets";
  import type { Tag } from "src/definitions/tag";
  import { getTags } from "src/lib/repositories/tags";

  export const load: Load = async ({ fetch, params }) => {
    const tags = await getTags({
      fetch,
      apiToken: get(apiToken),
    });

    const dataset = await getDatasetByID({
      fetch,
      apiToken: get(apiToken),
      id: params.id,
    });

    return {
      props: {
        dataset,
        tags,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { Dataset, DatasetFormData } from "src/definitions/datasets";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import paths from "$lib/paths";
  import { isAdmin, apiToken } from "$lib/stores/auth";
  import { deleteDataset } from "$lib/repositories/datasets";
  import { Maybe } from "$lib/util/maybe";
  import DatasetFormLayout from "src/lib/components/DatasetFormLayout/DatasetFormLayout.svelte";
  import type { SvelteComponent } from "svelte";
  import ModalExitFormConfirmation from "src/lib/components/ModalExitFormConfirmation/ModalExitFormConfirmation.svelte";

  export let dataset: Maybe<Dataset>;
  export let tags: Maybe<Tag[]>;

  let form: SvelteComponent;

  let modalTriggerId = "stop-editing-form-modal";

  let loading = false;

  let formHasBeenTouched = false;

  const history = window.history;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    if (!Maybe.Some(dataset)) {
      return;
    }

    const tagIds = event.detail.tags.map((item) => item.id);

    try {
      loading = true;

      const updatedDataset = await updateDataset({
        fetch,
        apiToken: $apiToken,
        id: dataset.id,
        data: { ...event.detail, tagIds },
      });

      if (Maybe.Some(updatedDataset)) {
        await goto(paths.datasetDetail({ id: updatedDataset.id }));
      }
    } finally {
      loading = false;
    }
  };

  const onClickDelete = async (): Promise<void> => {
    if (!Maybe.Some(dataset)) {
      return;
    }

    const confirmed = confirm(
      "Voulez-vous vraiment supprimer ce jeu de données ? Cette opération est irréversible."
    );

    if (!confirmed) {
      return;
    }

    await deleteDataset({ fetch, apiToken: $apiToken, id: dataset.id });
    await goto(paths.home);
  };

  const handleSaveAfterConfirmation = () => {
    form.submitForm();
  };
</script>

{#if Maybe.Some(dataset) && Maybe.Some(tags)}
  <header class="fr-p-4w">
    <h5>Modifier la fiche de jeu de données</h5>
    <button
      class="fr-btn fr-icon-close-line fr-btn--icon fr-btn--secondary"
      data-testid="exit-edit-form"
      data-fr-opened={false}
      aria-controls={formHasBeenTouched ? modalTriggerId : undefined}
      on:click={() => {
        if (!formHasBeenTouched) {
          history.back();
        }
      }}
    >
      {""}
    </button>
  </header>

  <ModalExitFormConfirmation
    {modalTriggerId}
    on:save={handleSaveAfterConfirmation}
  />

  <DatasetFormLayout>
    <DatasetForm
      bind:this={form}
      {tags}
      initial={dataset}
      {loading}
      submitLabel="Enregistrer les modifications"
      loadingLabel="Modification en cours..."
      on:save={onSave}
      on:touched={() => (formHasBeenTouched = true)}
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
