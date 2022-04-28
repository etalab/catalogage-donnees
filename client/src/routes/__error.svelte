<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";

  export const load: Load = ({ error, status }) => {
    return {
      props: {
        title: `${status}: ${error ? error.message : "unknown error"}`,
      },
    };
  };
</script>

<script lang="ts">
  export let title: string;
</script>

<section class="fr-container fr-mt-9w">
  <h1>{title}</h1>
</section>
