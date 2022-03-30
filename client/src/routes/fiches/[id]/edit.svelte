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

  export let dataset: Dataset;

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
</script>

<section class="fr-container fr-mt-9w">
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
  </div>
</section>
