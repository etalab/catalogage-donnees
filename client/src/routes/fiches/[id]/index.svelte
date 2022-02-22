<script lang="ts">
  import { page } from "$app/stores";

  const id = $page.params.id;

  const editUrl = `/fiches/${id}/edit`;
</script>

<h2 class="fr-mt-9w">Fiche de données</h2>

<div>
  <a href={editUrl} class="fr-link" title="Modifier cette fiche de données">
    Modifier
  </a>
</div>
