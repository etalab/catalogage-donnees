<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";
  import { apiToken } from "$lib/stores/auth";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";
  import { Maybe } from "$lib/util/maybe";

  let loading = false;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;

      const dataset = await createDataset({
        fetch,
        apiToken: $apiToken,
        data: event.detail,
      });

      if (Maybe.Some(dataset)) {
        await goto(paths.datasetDetail({ id: dataset.id }));
      }
    } finally {
      loading = false;
    }
  };
</script>

<svelte:head>
  <title>Contribuer</title>
</svelte:head>

<section class="fr-container fr-mt-9w">
  <h1 class="fr-text--lg">Contribuer un jeu de données</h1>

  <div class="fr-col-lg-8">
    <DatasetForm {loading} on:save={onSave} />
  </div>
</section>
