<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type { DatasetFormData } from "src/definitions/datasets";
  import { DATA_FORMAT_LABELS } from "src/constants";

  export let submitLabel = "Contribuer ce jeu de données";
  export let loadingLabel = "Contribution en cours...";
  export let loading = false;

  export let initial: DatasetFormData = {
    title: "",
    description: "",
    formats: [],
  };

  const dispatch = createEventDispatcher<{ save: DatasetFormData }>();

  type DatasetFormValues = {
    title: string;
    description: string;
    dataFormats: boolean[];
  };

  const dataFormatChoices = Object.entries(DATA_FORMAT_LABELS).map(
    ([value, label]) => ({ value, label })
  );

  const initialValues: DatasetFormValues = {
    title: initial.title,
    description: initial.description,
    dataFormats: dataFormatChoices.map(
      ({ value }) => !!initial.formats.find((v) => v === value)
    ),
  };

  // Handle this value manually.
  const dataFormatsValue = initialValues.dataFormats;

  const {
    form,
    errors,
    handleChange,
    handleSubmit,
    updateValidateField,
    isValid,
  } = createForm({
    initialValues,
    validationSchema: yup.object().shape({
      title: yup.string().required("Le titre ne peut être vide"),
      description: yup.string().required("La description ne peut être vide"),
      dataFormats: yup
        .array(yup.boolean())
        .length(dataFormatsValue.length)
        .test(
          "dataformats-some-checked",
          "Au moins un format de donnée doit être renseigné",
          (value) => value.some((checked) => !!checked)
        ),
    }),
    onSubmit: (values) => {
      const formats = [];
      values.dataFormats.forEach((checked, index) => {
        if (checked) {
          formats.push(dataFormatChoices[index].value);
        }
      });
      const data: DatasetFormData = {
        title: values.title,
        description: values.description,
        formats,
      };
      dispatch("save", data);
    },
  });

  const hasError = (error: string | string[]) => {
    return typeof error === "string" && Boolean(error);
  };

  const handleDataformatChange = (event, index: number) => {
    const { checked } = event.target;
    dataFormatsValue[index] = checked;
    updateValidateField("dataFormats", dataFormatsValue);
  };
</script>

<form on:submit={handleSubmit} data-bitwarden-watching="1">
  <fieldset class="fr-fieldset fr-my-4w">
    <div class="fr-input-group {$errors.title ? 'fr-input-group--error' : ''}">
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
          informations saisies ici seront utilisées par le moteur de recherche.
        </span>
      </label>
      <textarea
        class="fr-input {$errors.description ? 'fr-input--error' : ''}"
        aria-describedby={$errors.description ? "description-desc-error" : null}
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
        {@const id = `dataformats-${value}`}
        <div class="fr-checkbox-group">
          <input
            type="checkbox"
            {id}
            name="dataformats"
            {value}
            checked={dataFormatsValue[index]}
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
      {#if loading}
        {loadingLabel}
      {:else}
        {submitLabel}
      {/if}
    </button>
  </div>
</form>
