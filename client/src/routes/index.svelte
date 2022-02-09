<script lang="ts">
  import { createForm } from "svelte-forms-lib";
  import * as yup from "yup";
  import { getApiUrl } from "$lib/fetch";

  const postData = async (values) => {
    const data = JSON.stringify(values);
    const url = `${getApiUrl()}/datasets/`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: data,
    });
    await new Promise((r) => setTimeout(r, 1000)); // TODO: remove, just for debugging purposes
    return await response.json();
  };

  const { form, errors, handleChange, handleSubmit, isSubmitting, isValid } =
    createForm({
      initialValues: {
        title: "",
        description: "",
      },
      validationSchema: yup.object().shape({
        title: yup.string().required("Le titre ne peut être vide"),
        description: yup.string().required("La description ne peut être vide"),
      }),
      onSubmit: (values) => {
        const result = postData(values);
        return result;
      },
    });
  const errorClassname = (error: string, className: string) =>
    error ? className : "";
</script>

<h1>Informations générales</h1>
<div class="fr-col fr-col-lg-8">
  <form on:submit={handleSubmit} data-bitwarden-watching="1">
    <fieldset class="fr-fieldset fr-my-4w">
      <div
        class="fr-input-group {errorClassname(
          $errors.title,
          'fr-input-group--error'
        )}"
      >
        <label class="fr-label mandatory" for="title">
          Nom de la donnée
          <span class="fr-hint-text" id="select-hint-desc-hint">
            Ce nom doit aller à l’essentiel et permettre d’indiquer en quelques
            mots les informations que l’on peut y trouver.
          </span>
        </label>
        <input
          class="fr-input {errorClassname($errors.title, 'fr-input--error')}"
          aria-describedby={$errors.title ? "title-desc-error" : null}
          type="text"
          id="title"
          name="title"
          on:change={handleChange}
          on:blur={handleChange}
          bind:value={$form.title}
        />
        {#if $errors.title}
          <p id="title-desc-error" class="fr-error-text">
            {$errors.title}
          </p>
        {/if}
      </div>

      <div
        class="fr-input-group {errorClassname(
          $errors.description,
          'fr-input-group--error'
        )}"
      >
        <label class="fr-label mandatory" for="description">
          Description des données
          <span class="fr-hint-text" id="select-hint-desc-hint">
            Quel type de données sont contenues dans ce jeu de données ? Les
            informations saisies ici seront utilisées par le moteur de
            recherche.
          </span>
        </label>
        <textarea
          class="fr-input {errorClassname(
            $errors.description,
            'fr-input--error'
          )}"
          aria-describedby={$errors.description
            ? "description-desc-error"
            : null}
          id="description"
          name="description"
          on:change={handleChange}
          on:blur={handleChange}
          bind:value={$form.description}
        />
        {#if $errors.description}
          <p id="description-desc-error" class="fr-error-text">
            {$errors.description}
          </p>
        {/if}
      </div>
    </fieldset>

    <div class="fr-input-group fr-my-4w">
      <button
        type="submit"
        disabled={!$isValid}
        class="fr-btn"
        title="Contribuer ce jeu de données"
      >
        {#if $isSubmitting}
          Contribution en cours...
        {:else}
          Contribuer ce jeu de données
        {/if}
      </button>
    </div>
  </form>
</div>
