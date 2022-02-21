<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { getDatasetByID } from "$lib/repositories/datasets";

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
  import type { Dataset, DatasetFormData } from "src/definitions/datasets";
  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";

  export let dataset: Dataset;
  const onSave = async (event: CustomEvent<DatasetFormData>) => {};
</script>

<h1>Modifier "{dataset.title}"</h1>

<h2>Informations générales</h2>

<section class="fr-col-lg-8">
  <DatasetForm
    initial={{ title: dataset.title, description: dataset.description, formats: dataset.formats }}
    on:save={onSave}
  />
</section>
