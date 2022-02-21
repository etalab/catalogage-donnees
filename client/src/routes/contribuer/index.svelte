<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import type { DatasetFormData } from "src/definitions/datasets";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";

  let loading = false;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      await createDataset({ fetch, data: event.detail });
    } finally {
      loading = false;
    }
  };
</script>

<svelte:head>
  <title>Contribuer</title>
</svelte:head>

<h1>Informations générales</h1>
<div class="fr-col-lg-8">
  <DatasetForm {loading} on:save={onSave} />
</div>
