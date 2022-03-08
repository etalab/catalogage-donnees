<script lang="ts">
  import { page } from "$app/stores";
  import paths from "$lib/paths";

  const id = $page.params.id;

  const editUrl = paths.datasetEdit({ id });
</script>

<section class="fr-container fr-mt-9w">
  <h2>Fiche de données</h2>

  <div>
    <a href={editUrl} class="fr-link" title="Modifier cette fiche de données">
      Modifier
    </a>
  </div>
</section>
