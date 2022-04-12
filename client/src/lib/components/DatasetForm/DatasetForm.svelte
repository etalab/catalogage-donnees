<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type { DataFormat, DatasetFormData } from "src/definitions/datasets";
  import { DATA_FORMAT_LABELS, UPDATE_FREQUENCY } from "src/constants";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import { user } from "src/lib/stores/auth";
  import ContactEmailsField from "../ContactEmailsField/ContactEmailsField.svelte";

  export let submitLabel = "Publier ce jeu de données";
  export let loadingLabel = "Publication en cours...";
  export let loading = false;

  export let initial: DatasetFormData = {
    title: "",
    description: "",
    formats: [],
    entrypointEmail: "",
    contactEmails: [$user?.email] || [""],
    service: "",
    lastUpdatedAt: "",
    updateFrequency: "",
  };

  const dispatch = createEventDispatcher<{ save: DatasetFormData }>();

  type DatasetFormValues = {
    title: string;
    description: string;
    dataFormats: boolean[];
    entrypointEmail: string;
    contactEmails: string[];
    service: string;
    lastUpdatedAt: string;
    updateFrequency: string;
  };

  const dataFormatChoices = Object.entries(DATA_FORMAT_LABELS).map(
    ([value, label]: [DataFormat, string]) => ({ value, label })
  );

  const initialValues: DatasetFormValues = {
    title: initial.title,
    description: initial.description,
    dataFormats: dataFormatChoices.map(
      ({ value }) => !!initial.formats.find((v) => v === value)
    ),
    entrypointEmail: initial.entrypointEmail,
    contactEmails: initial.contactEmails,
    service: initial.service,
    lastUpdatedAt: initial.lastUpdatedAt,
    updateFrequency: initial.updateFrequency,
  };

  // Handle this value manually.
  const dataFormatsValue = initialValues.dataFormats;

  const { form, errors, handleChange, handleSubmit, updateValidateField } =
    createForm({
      initialValues,
      validationSchema: yup.object().shape({
        title: yup.string().required("Ce champs est requis"),
        description: yup.string().required("Ce champs est requis"),
        dataFormats: yup.array(yup.boolean()).length(dataFormatsValue.length),
        entrypointEmail: yup
          .string()
          .email("Ce champ doit contenir une adresse e-mail valide")
          .required("Ce champs est requis"),
        contactEmails: yup
          .array()
          .of(
            yup
              .string()
              .email("Ce champ doit contenir une adresse e-mail valide")
          ),
        service: yup.string().required("Ce champs est requis"),
        lastUpdatedAt: yup.date().required("Ce champs est requis"),
        updateFrequency: yup.string().required("Ce champs est requis"),
      }),
      onSubmit: (values) => {
        const formats = values.dataFormats
          .map((checked, index) =>
            checked ? dataFormatChoices[index].value : null
          )
          .filter(Boolean);

        const contactEmails = values.contactEmails.filter(Boolean);

        const data: DatasetFormData = {
          ...values,
          formats,
          contactEmails,
        };

        dispatch("save", data);
      },
    });

  $: saveBtnLabel = loading ? loadingLabel : submitLabel;

  $: emailErrors = $errors.contactEmails as unknown as string[];

  const hasError = (error: string | string[]) => {
    return typeof error === "string" && Boolean(error);
  };

  const handleDataformatChange = (event: Event, index: number) => {
    const { checked } = event.target as HTMLInputElement;
    dataFormatsValue[index] = checked;
    updateValidateField("dataFormats", dataFormatsValue);
  };
</script>

<form on:submit={handleSubmit} data-bitwarden-watching="1">
  <h2 class="fr-mt-6w">Informations générales</h2>

  <div
    class="fr-input-group fr-my-4w {$errors.title
      ? 'fr-input-group--error'
      : ''}"
  >
    <label class="fr-label" for="title">
      Nom de la donnée
      <RequiredMarker />
      <span class="fr-hint-text" id="title-desc-hint">
        Ce nom doit aller à l'essentiel et permettre d'indiquer en quelques mots
        les informations que l'on peut y trouver.
      </span>
    </label>
    <input
      class="fr-input {$errors.title ? 'fr-input--error' : ''}"
      aria-describedby={$errors.title ? "title-desc-error" : null}
      type="text"
      id="title"
      name="title"
      required
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
    class="fr-input-group fr-my-4w {$errors.description
      ? 'fr-input-group--error'
      : ''}"
  >
    <label class="fr-label" for="description">
      Description des données
      <RequiredMarker />
      <span class="fr-hint-text" id="description-desc-hint">
        Quel type de données sont contenues dans ce jeu de données ? Les
        informations saisies ici seront utilisées par le moteur de recherche.
      </span>
    </label>
    <textarea
      class="fr-input {$errors.description ? 'fr-input--error' : ''}"
      aria-describedby={$errors.description ? "description-desc-error" : null}
      id="description"
      name="description"
      required
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
      <RequiredMarker />
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
            required={dataFormatsValue.every((checked) => !checked)}
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

  <h2 class="fr-mt-6w">Contacts</h2>
  <p class="fr-text--md">
    Dans un soucis de traçabilité et de facilité de mise à jour, il est
    fondamental de pouvoir prendre contact avec l’organisation ou les personnes
    productrices d’une donnée. Lorsqu’une demande de contact sera effectuée,
    l’ensemble des adresses e-mail saisies recevront la notification.
  </p>
  <div
    class="fr-input-group fr-my-4w {$errors.service
      ? 'fr-input-group--error'
      : ''}"
  >
    <label class="fr-label" for="service">
      Service producteur de la donnée
      <RequiredMarker />
    </label>
    <input
      class="fr-input {$errors.service ? 'fr-input--error' : ''}"
      aria-describedby={$errors.service
        ? "entrypoint-service-desc-error"
        : null}
      type="text"
      id="service"
      name="service"
      required
      on:change={handleChange}
      on:blur={handleChange}
      bind:value={$form.service}
    />

    {#if $errors.service}
      <p id="title-desc-error" class="fr-error-text">
        {$errors.service}
      </p>
    {/if}
  </div>

  <div
    class="fr-input-group fr-my-4w {$errors.entrypointEmail
      ? 'fr-input-group--error'
      : ''}"
  >
    <label class="fr-label" for="entrypointEmail">
      Adresse e-mail fonctionnelle
      <RequiredMarker />
      <span class="fr-hint-text" id="entrypointEmail-desc-hint">
        Il est fortement conseillé d'avoir une adresse e-mail accessible à
        plusieurs personnes afin de rendre la prise de contact possible quelle
        que soit les personnes en responsabilité.
      </span>
    </label>
    <input
      class="fr-input {$errors.entrypointEmail ? 'fr-input--error' : ''}"
      aria-describedby={$errors.entrypointEmail
        ? "entrypointEmail-desc-error"
        : null}
      type="email"
      id="entrypointEmail"
      name="entrypointEmail"
      required
      on:change={handleChange}
      on:blur={handleChange}
      bind:value={$form.entrypointEmail}
    />
    {#if $errors.entrypointEmail}
      <p id="entrypoint-email-desc-error" class="fr-error-text">
        {$errors.entrypointEmail}
      </p>
    {/if}
  </div>

  <ContactEmailsField
    bind:errors={emailErrors}
    bind:contactEmails={$form.contactEmails}
    on:blur={handleChange}
    on:change={handleChange}
  />

  <h2 class="fr-mt-6w">Mise à jour</h2>

  <p class="fr-text--md">
    A moins qu’il ne soit une production ponctuelle, un jeu de donnée n’est
    utile que lorsqu’il est à jour ! Avec ces quelques informations nous
    pourrons indiquer à vos réutilisateurs lorsque les données seront mises à
    jour.
  </p>

  <div
    class="fr-input-group fr-my-4w {$errors.lastUpdatedAt
      ? 'fr-input-group--error'
      : ''}"
  >
    <label class="fr-label" for="lastUpdatedAt">
      Date de la dernière mise à jour
      <RequiredMarker />
    </label>

    <div class="fr-input-wrap fr-fi-calendar-line">
      <input
        class="fr-input {$errors.lastUpdatedAt ? 'fr-input--error' : ''}"
        aria-describedby={$errors.lastUpdatedAt
          ? "entrypoint-service-desc-error"
          : null}
        type="date"
        id="lastUpdatedAt"
        name="lastUpdatedAt"
        required
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={$form.lastUpdatedAt}
      />

      {#if $errors.lastUpdatedAt}
        <p id="title-desc-error" class="fr-error-text">
          {$errors.lastUpdatedAt}
        </p>
      {/if}
    </div>
  </div>

  <div class="fr-select-group">
    <label class="fr-label" for="updateFrequency"
      >Fréquence de mise à jour <RequiredMarker /></label
    >
    <select
      class="fr-select"
      required
      bind:value={$form.updateFrequency}
      id="updateFrequency"
      name="updateFrequency"
      on:change={handleChange}
      on:blur={handleChange}
    >
      <option value="" selected disabled hidden>Sélectionner une option</option>
      {#each Object.keys(UPDATE_FREQUENCY) as frequency}
        <option value={frequency}>{UPDATE_FREQUENCY[frequency]}</option>
      {/each}
    </select>

    {#if $errors.updateFrequency}
      <p id="title-desc-error" class="fr-error-text">
        {$errors.updateFrequency}
      </p>
    {/if}
  </div>

  <div class="fr-input-group fr-mt-9w">
    <button type="submit" class="fr-btn">
      {saveBtnLabel}
    </button>
  </div>
</form>
