<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type { LoginFormData, User } from "src/definitions/auth";
  import { login } from "$lib/repositories/auth";

  let loading = false;
  let loginFailed = false;

  const dispatch = createEventDispatcher<{ login: User }>();

  const onSubmit = async (data: LoginFormData) => {
    try {
      loading = true;
      loginFailed = false;

      const response = await login({ fetch, data });
      loginFailed = response.status === 401;

      if (loginFailed) {
        return;
      }

      const user: User = {
        email: response.data.email,
        apiToken: response.data.apiToken,
      };

      dispatch("login", user);
    } finally {
      loading = false;
    }
  };

  const { form, errors, handleChange, handleSubmit, isValid } =
    createForm<LoginFormData>({
      initialValues: {
        email: "",
        password: "",
      },
      validationSchema: yup.object().shape({
        email: yup
          .string()
          .email("Ce champ doit être un e-mail valide")
          .required("Ce champ est obligatoire"),
        password: yup.string().required("Ce champ est obligatoire"),
      }),
      onSubmit: async (values) => {
        const data = { ...values };
        await onSubmit(data);
      },
    });

  $: hasEmailError = $errors.email || loginFailed;
  $: hasPasswordError = $errors.password || loginFailed;
</script>

<form on:submit|preventDefault={handleSubmit} data-bitwarden-watching="1">
  <fieldset class="fr-fieldset fr-my-4w">
    <div class="fr-input-group {hasEmailError ? 'fr-input-group--error' : ''}">
      <label for="email" class="fr-label"> Adresse e-mail </label>
      <input
        class="fr-input {hasEmailError ? 'fr-input--error' : ''}"
        aria-describedby={$errors.email ? "email-desc-error" : null}
        type="email"
        id="email"
        name="email"
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={$form.email}
      />
      {#if $errors.email}
        <p id="email-desc-error" class="fr-error-text">
          {$errors.email}
        </p>
      {/if}
    </div>

    <div
      class="fr-input-group {hasPasswordError ? 'fr-input-group--error' : ''}"
    >
      <label for="password" class="fr-label"> Mot de passe </label>
      <input
        class="fr-input {hasPasswordError ? 'fr-input--error' : ''}"
        aria-describedby={$errors.password ? "password-desc-error" : null}
        type="password"
        id="password"
        name="password"
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={$form.password}
      />
      {#if $errors.password}
        <p id="password-desc-error" class="fr-error-text">
          {$errors.password}
        </p>
      {/if}
    </div>

    {#if loginFailed}
      <p class="fr-error-text">Adresse e-mail ou identifiant invalide</p>
    {/if}
  </fieldset>

  <div class="fr-grid-row fr-grid-row--center">
    <button
      class="fr-btn fr-btn--icon-right fr-fi-logout-box-r-line"
      type="submit"
      disabled={!$isValid}
      title="Se connecter"
    >
      {#if loading}
        Connexion en cours...
      {:else}
        Se connecter
      {/if}
    </button>
  </div>
</form>
