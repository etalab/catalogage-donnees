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

  export let dataset: Maybe<Dataset>;
  export let tags: Tag[];

  let loading = false;

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
</script>

{#if Maybe.Some(dataset) && Maybe.Some(tags)}
  <header class="fr-m-4w">
    <h5>Modifier le jeu de donnée</h5>

    <a
      aria-label="go to fiche page"
      href="/fiches/{dataset.id}"
      title="Aller vers la jeu de donnée"
      class="fr-btn fr-fi-close-line fr-btn--icon fr-btn--secondary"
    >
      {""}
    </a>
  </header>
  <DatasetFormLayout>
    <DatasetForm
      {tags}
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
  </DatasetFormLayout>
{/if}

<style>
  header {
    display: flex;
    justify-content: space-between;
  }
</style>
