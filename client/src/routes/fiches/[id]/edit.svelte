<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { getDatasetByID, updateDataset } from "$lib/repositories/datasets";

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
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import type { Dataset, DatasetFormData } from "src/definitions/datasets";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import paths from "$lib/paths";
  import { isAdmin, apiToken } from "$lib/stores/auth";
  import { deleteDataset } from "$lib/repositories/datasets";

  export let dataset: Dataset;

  const id = $page.params.id;
  let loading = false;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      await updateDataset({
        fetch,
        apiToken: $apiToken,
        id,
        data: event.detail,
      });
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

    await deleteDataset({ fetch, apiToken: $apiToken, id: dataset.id });
    await goto(paths.home);
  };
</script>

<section class="fr-container fr-my-9w">
  <h1 class="fr-text--lg">
    Modifier "{dataset.title}"
  </h1>

  <div class="fr-col-lg-8">
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
</section>
