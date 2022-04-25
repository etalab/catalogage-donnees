<script lang="ts" context="module">
  export const prerender = true;
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { LoginFormData, User } from "src/definitions/auth";
  import { login } from "$lib/stores/auth";
  import { login as sendLoginRequest } from "$lib/repositories/auth";
  import LoginForm from "$lib/components/LoginForm/LoginForm.svelte";

  let loading = false;
  let loginFailed = false;

  const onSubmit = async (event: CustomEvent<LoginFormData>) => {
    try {
      loading = true;
      loginFailed = false;

      const response = await sendLoginRequest({ fetch, data: event.detail });
      loginFailed = response.status === 401;

      if (loginFailed) {
        return;
      }

      const user: User = {
        email: response.data.email,
        role: response.data.role,
        apiToken: response.data.apiToken,
      };

      login(user);
      await goto("/");
    } finally {
      loading = false;
    }
  };
</script>

<svelte:head>
  <title>Connexion</title>
</svelte:head>

<section class="fr-container fr-mb-15w">
  <h1 class="fr-grid-row fr-grid-row--center fr-mt-6w">
    Bienvenue sur votre outil de catalogage de données
  </h1>

  <p class="fr-grid-row fr-grid-row--center fr-text--lead fr-mt-6w">
    Connectez-vous à l'espace (démonstration)
  </p>

  <div class="fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-md-6">
      <LoginForm {loading} {loginFailed} on:submit={onSubmit} />
    </div>
  </div>
</section>
