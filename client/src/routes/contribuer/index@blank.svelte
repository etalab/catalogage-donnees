<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  export const prerender = true;
  import { getTags } from "src/lib/repositories/tags";
  import { apiToken } from "$lib/stores/auth";
  import { get } from "svelte/store";
  export const load: Load = async ({ fetch }) => {
    const tags = await getTags({
      fetch,
      apiToken: get(apiToken),
    });
    return {
      props: {
        tags,
      },
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { DatasetFormData } from "src/definitions/datasets";
  import paths from "$lib/paths";

  import DatasetForm from "$lib/components/DatasetForm/DatasetForm.svelte";
  import { createDataset } from "$lib/repositories/datasets";
  import { Maybe } from "$lib/util/maybe";
  import DatasetFormLayout from "src/lib/components/DatasetFormLayout/DatasetFormLayout.svelte";
  import type { Tag } from "src/definitions/tag";

  let loading = false;

  export let tags: Maybe<Tag[]>;

  const onSave = async (event: CustomEvent<DatasetFormData>) => {
    try {
      loading = true;
      const tagIds = event.detail.tags.map((item) => item.id);
      const dataset = await createDataset({
        fetch,
        apiToken: $apiToken,
        data: { tagIds, ...event.detail },
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

{#if Maybe.Some(tags)}
  <DatasetFormLayout>
    <DatasetForm {tags} {loading} on:save={onSave} />
  </DatasetFormLayout>
{/if}

<style>
  header {
    display: flex;
    justify-content: space-between;
  }
</style>
