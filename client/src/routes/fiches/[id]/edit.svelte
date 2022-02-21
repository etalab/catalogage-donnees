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

  export let dataset: Dataset;

  const id = $page.params.id;

  let loading = false;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      await updateDataset({ fetch, id, data: event.detail });
      await goto(`/fiches/${id}`);
    } finally {
      loading = false;
    }
  };
</script>

<h1>Modifier "{dataset.title}"</h1>

<h2>Informations générales</h2>

<section class="fr-col-lg-8">
  <DatasetForm
    initial={{
      title: dataset.title,
      description: dataset.description,
      formats: dataset.formats,
    }}
    {loading}
    submitLabel="Modifier ce jeu de données"
    loadingLabel="Modification en cours..."
    on:save={onSave}
  />
</section>
