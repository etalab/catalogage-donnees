<script context="module" lang="ts">
  export const prerender = true;
</script>

<script lang="ts">
  import { createForm } from "svelte-forms-lib";
  import * as yup from "yup";
  import { createDataset } from "$lib/repositories/datasets";
  import { DATA_FORMAT_LABELS } from "src/constants";

  const dataFormatChoices = Object.entries(DATA_FORMAT_LABELS).map(
    ([value, label]) => ({ value, label })
  );

  const dataFormatSelected = dataFormatChoices.map(() => false);

  const {
    form,
    errors,
    handleChange,
    handleSubmit,
    updateValidateField,
    isSubmitting,
    isValid,
  } = createForm({
    initialValues: {
      title: "",
      description: "",
      dataFormats: [] as boolean[],
    },
    validationSchema: yup.object().shape({
      title: yup.string().required("Le titre ne peut être vide"),
      description: yup.string().required("La description ne peut être vide"),
      dataFormats: yup
        .array(yup.boolean())
        .length(dataFormatSelected.length)
        .test(
          "dataformats-some-checked",
          "Au moins un format de donnée doit être renseigné",
          (value) => value.some((checked) => !!checked)
        ),
    }),
    onSubmit: async (values) => {
      const formats = [];
      values.dataFormats.forEach((checked, index) => {
        if (checked) {
          formats.push(dataFormatChoices[index].value);
        }
      });
      const payload = {
        title: values.title,
        description: values.description,
        formats,
      };
      const body = JSON.stringify(payload);
      return await createDataset({ fetch, body });
    },
  });

  const hasError = (error: string | string[]) => {
    return typeof error === "string" && Boolean(error);
  };

  const handleDataformatChange = (event, index: number) => {
    const { checked } = event.target;
    dataFormatSelected[index] = checked;
    updateValidateField("dataFormats", dataFormatSelected);
  };
</script>

<svelte:head>
  <title>Contribuer</title>
</svelte:head>

<h1>Informations générales</h1>
<div class="fr-col-lg-8">
  <form on:submit={handleSubmit} data-bitwarden-watching="1">
    <fieldset class="fr-fieldset fr-my-4w">
      <div
        class="fr-input-group {$errors.title ? 'fr-input-group--error' : ''}"
      >
        <label class="fr-label mandatory" for="title">
          Nom de la donnée
          <span class="fr-hint-text" id="select-hint-desc-hint">
            Ce nom doit aller à l’essentiel et permettre d’indiquer en quelques
            mots les informations que l’on peut y trouver.
          </span>
        </label>
        <input
          class="fr-input {$errors.title ? 'fr-input--error' : ''}"
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
        class="fr-input-group {$errors.description
          ? 'fr-input-group--error'
          : ''}"
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
          class="fr-input {$errors.description ? 'fr-input--error' : ''}"
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

    <fieldset
      class="fr-fieldset {hasError($errors.dataFormats)
        ? 'fr-fieldset--error'
        : ''}"
      aria-describedby={hasError($errors.dataFormats)
        ? "dataformats-desc-error"
        : null}
      role="group"
    >
      <legend
        class="fr-fieldset__legend fr-text--regular"
        id="dataformats-hint-legend"
      >
        Format(s) des données
        <span class="fr-hint-text" id="select-hint-dataformats-hint">
          Sélectionnez ici les différents formats de données qu'un réutilisateur
          potentiel pourrait exploiter.
        </span>
      </legend>
      <div class="fr-fieldset__content">
        {#each dataFormatChoices as { value, label }, index (value)}
          {@const id = `dataformats-${index}`}
          <div class="fr-checkbox-group">
            <input
              type="checkbox"
              {id}
              name="dataformats"
              {value}
              on:blur={(event) => handleDataformatChange(event, index)}
              on:change={(event) => handleDataformatChange(event, index)}
            />
            <label for={id}>
              {label}
            </label>
          </div>
        {/each}
      </div>
      {#if hasError($errors.dataFormats)}
        <p id="dataformats-desc-error" class="fr-error-text">
          {$errors.dataFormats}
        </p>
      {/if}
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
