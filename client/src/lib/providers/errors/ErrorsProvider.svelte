<script lang="ts">
  import { goto } from "$app/navigation";
  import paths from "$lib/paths";
  import { apiErrors } from "$lib/stores/errors";
  import { logout } from "$lib/stores/auth";
  import { Maybe } from "$lib/util/maybe";
  import { onDestroy } from "svelte";

  const unsubscribe = apiErrors.subscribe(async (error) => {
    if (!Maybe.Some(error)) {
      return;
    }

    if (error.status === 401) {
      // We failed to authenticate with the API.
      // * If we passed credentials when calling the API, it means these
      //   credentials have become invalid, so we should log the user out
      //   and invite them to log in again.
      // * If we did not pass credentials (e.g. API was called from a public
      //   page), it still means the client tried to access a protected
      //   resource, so we need the user to authenticate.
      logout();
      await goto(paths.login);
    }
  });

  onDestroy(unsubscribe);
</script>

<slot />
