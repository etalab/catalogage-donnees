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
  import DatasetFormLayout from "src/lib/components/DatasetFormLayout/DatasetFormLayout.svelte";

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

<header class="fr-m-4w">
  <h5>Modifier le jeu de donnée</h5>
  <a
    aria-label="go to home page"
    href="/"
    class="fr-btn fr-fi-close-line fr-btn--icon fr-btn--secondary"
  >
    {""}
  </a>
</header>

<DatasetFormLayout>
  <DatasetForm {loading} on:save={onSave} />
</DatasetFormLayout>

<style>
  header {
    display: flex;
    justify-content: space-between;
  }
</style>
