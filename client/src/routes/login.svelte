<script lang="ts" context="module">
  export const prerender = true;
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import type { User } from "src/definitions/auth";
  import LoginForm from "$lib/components/LoginForm/LoginForm.svelte";
  import { login } from "$lib/stores/auth";

  const onLogin = async (event: CustomEvent<User>) => {
    login(event.detail);
    await goto("/");
  };
</script>

<svelte:head>
  <title>Connexion</title>
</svelte:head>

<section class="fr-container">
  <h1 class="fr-grid-row fr-grid-row--center fr-mt-6w">
    Bienvenue sur votre outil de catalogage de données
  </h1>

  <p class="fr-grid-row fr-grid-row--center fr-text--lead fr-mt-6w">
    Connectez-vous à l'espace (démonstration)
  </p>

  <div class="fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-md-6">
      <LoginForm on:login={onLogin} />
    </div>
  </div>
</section>
