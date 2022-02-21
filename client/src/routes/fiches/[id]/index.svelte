<script lang="ts">
  import { page } from "$app/stores";

  $: editUrl = `/fiches/${$page.params.id}/edit`;
</script>

<h2>Fiche de données</h2>

<div>
  <a href={editUrl} class="fr-link" title="Modifier cette fiche de données">
    Modifier
  </a>
</div>
