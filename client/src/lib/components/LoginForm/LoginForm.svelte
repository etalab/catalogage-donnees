<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type { LoginFormData } from "src/definitions/auth";

  export let loading = false;
  export let loginFailed = false;

  const dispatch = createEventDispatcher<{ submit: LoginFormData }>();

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
      onSubmit: (values) => {
        dispatch("submit", values);
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
