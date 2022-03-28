<script lang="ts" context="module">
  import type { ErrorLoad } from "@sveltejs/kit";

  export const load: ErrorLoad = ({ error, status }) => {
    return {
      props: {
        title: `${status}: ${error.message}`,
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
