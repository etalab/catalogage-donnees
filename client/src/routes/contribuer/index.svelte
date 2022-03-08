<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";

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

<section class="fr-container">
  <h1 class="fr-mt-9w">Informations générales</h1>

  <div class="fr-col-lg-8">
    <DatasetForm {loading} on:save={onSave} />
  </div>
</section>
