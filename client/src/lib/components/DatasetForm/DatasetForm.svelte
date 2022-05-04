<script lang="ts">
  import * as yup from "yup";
  import { createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";
  import type {
    DataFormat,
    DatasetFormData,
    GeographicalCoverage,
    UpdateFrequency,
  } from "src/definitions/datasets";
  import {
    DATA_FORMAT_LABELS,
    UPDATE_FREQUENCY_LABELS,
    GEOGRAPHICAL_COVERAGE_LABELS,
  } from "src/constants";
  import { formatHTMLDate } from "$lib/util/format";
  import RequiredMarker from "../RequiredMarker/RequiredMarker.svelte";
  import { user } from "src/lib/stores/auth";
  import ContactEmailsField from "../ContactEmailsField/ContactEmailsField.svelte";
  import Select from "../Select/Select.svelte";
  import { toSelectOptions } from "src/lib/transformers/form";
  import { handleSelectChange } from "src/lib/util/form";
  import { type DropMaybe, Maybe, type AddMaybe } from "$lib/util/maybe";
  import TagSelector from "../TagSelector/TagSelector.svelte";
  import type { Tag } from "src/definitions/tag";

  export let submitLabel = "Publier ce jeu de données";
  export let loadingLabel = "Publication en cours...";
  export let loading = false;
  export let tags: Tag[] = [];

  export let initial: AddMaybe<DatasetFormData, "geographicalCoverage"> = {
    title: "",
    description: "",
    service: "",
    formats: [],
    producerEmail: "",
    contactEmails: [$user?.email || ""],
    geographicalCoverage: null, // Allow select null option upon creation
    lastUpdatedAt: null,
    updateFrequency: null,
    technicalSource: "",
    publishedUrl: null,
    tags: [],
  };

  const dispatch = createEventDispatcher<{ save: DatasetFormData }>();

  type DatasetFormValues = {
    title: string;
    description: string;
    service: string;
    dataFormats: boolean[];
    producerEmail: string | null;
    contactEmails: string[];
    geographicalCoverage: Maybe<GeographicalCoverage>;
    lastUpdatedAt: string | null;
    updateFrequency: UpdateFrequency | null;
    technicalSource: string | null;
    publishedUrl: string | null;
    tags: Tag[];
  };

  const dataFormatChoices = Object.entries(DATA_FORMAT_LABELS).map(
    ([value, label]: [DataFormat, string]) => ({ value, label })
  );

  const initialValues: DatasetFormValues = {
    title: initial.title,
    description: initial.description,
    service: initial.service,
    dataFormats: dataFormatChoices.map(
      ({ value }) => !!initial.formats.find((v) => v === value)
    ),
    producerEmail: initial.producerEmail,
    contactEmails: initial.contactEmails,
    lastUpdatedAt: initial.lastUpdatedAt
      ? formatHTMLDate(initial.lastUpdatedAt)
      : null,
    geographicalCoverage: initial.geographicalCoverage,
    updateFrequency: initial.updateFrequency,
    technicalSource: initial.technicalSource,
    publishedUrl: initial.publishedUrl,
    tags: initial.tags,
  };

  // Handle this value manually.
  const dataFormatsValue = initialValues.dataFormats;

  const { form, errors, handleChange, handleSubmit, updateValidateField } =
    createForm({
      initialValues,
      validationSchema: yup.object().shape({
        title: yup.string().required("Ce champs est requis"),
        description: yup.string().required("Ce champs est requis"),
        service: yup.string().required("Ce champs est requis"),
        dataFormats: yup.array(yup.boolean()).length(dataFormatsValue.length),
        producerEmail: yup
          .string()
          .email("Ce champ doit contenir une adresse e-mail valide")
          .nullable(),
        contactEmails: yup
          .array()
          .of(
            yup
              .string()
              .email("Ce champ doit contenir une adresse e-mail valide")
          )
          .min(1),
        lastUpdatedAt: yup.date().nullable(),
        updateFrequency: yup.string().nullable(),
        geographicalCoverage: yup
          .string()
          .nullable()
          .required("Ce champs est requis"),
        technicalSource: yup.string().nullable(),
        publishedUrl: yup.string().nullable(),
        tags: yup
          .array()
          .of(
            yup.object().shape({
              name: yup.string(),
              id: yup.string(),
            })
          )
          .min(1, "Veuillez séléctionner au moins 1 mot-clé"),
      }),
      onSubmit: (
        values: DropMaybe<DatasetFormValues, "geographicalCoverage">
      ) => {
        const formats = values.dataFormats
          .map((checked, index) =>
            checked ? dataFormatChoices[index].value : null
          )
          .filter(Maybe.Some);

        // Ensure "" becomes null.
        const producerEmail = values.producerEmail
          ? values.producerEmail
          : null;

        const contactEmails = values.contactEmails.filter(Boolean);

        const lastUpdatedAt = values.lastUpdatedAt
          ? new Date(values.lastUpdatedAt)
          : null;

        const data: DatasetFormData = {
          ...values,
          formats,
          producerEmail,
          contactEmails,
          lastUpdatedAt,
        };

        dispatch("save", data);
      },
    });

  $: saveBtnLabel = loading ? loadingLabel : submitLabel;

  $: emailErrors = $errors.contactEmails as unknown as string[];

  // the tag error returned by yup could be a string, an array of string,  or an object with the same shape of Tag
  $: hasTagsError = typeof $errors.tags === "string" && !!$errors.tags;

  const hasError = (error: string | string[]) => {
    return typeof error === "string" && Boolean(error);
  };

  const handleDataformatChange = (event: Event, index: number) => {
    const { checked } = event.target as HTMLInputElement;
    dataFormatsValue[index] = checked;
    updateValidateField("dataFormats", dataFormatsValue);
  };

  const handleLastUpdatedAtChange = async (
    event: Event & { currentTarget: EventTarget & HTMLInputElement }
  ) => {
    if (!event.currentTarget.value /* Empty date */) {
      // Needs manual handling, otherwise yup would call e.g. new Date("") which is invalid.
      updateValidateField("lastUpdatedAt", null);
    } else {
      await handleChange(event);
    }
  };

  const handleTagsChange = async (event: CustomEvent<Tag[]>) => {
    updateValidateField("tags", event.detail);
  };
</script>

<form
  on:submit={handleSubmit}
  data-bitwarden-watching="1"
  aria-label="Informations sur le jeu de données"
>
  <h2 id="information-generales" class="fr-mb-5w">Informations générales</h2>

  <div class="form--content fr-mb-8w">
    <div
      class="fr-input-group fr-mb-4w {$errors.title
        ? 'fr-input-group--error'
        : ''}"
    >
      <label class="fr-label" for="title">
        Nom du jeu de la donnée
        <RequiredMarker />
        <span class="fr-hint-text" id="title-desc-hint">
          Ce nom doit aller à l'essentiel et permettre d'indiquer en quelques
          mots les informations que l'on peut y trouver.
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
        Description du jeu de données
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

    <Select
      options={toSelectOptions(GEOGRAPHICAL_COVERAGE_LABELS)}
      id="geographicalCoverage"
      name="geographicalCoverage"
      hintText="Quelle est l'étendue de la zone couverte par votre jeu de données ?"
      required
      label="Couverture géographique"
      placeholder="Sélectionnez une couverture géographique..."
      bind:value={$form.geographicalCoverage}
      on:change={(event) =>
        handleSelectChange(
          "geographicalCoverage",
          event,
          handleChange,
          updateValidateField
        )}
      on:blur={(event) =>
        handleSelectChange(
          "geographicalCoverage",
          event,
          handleChange,
          updateValidateField
        )}
      error={$errors.geographicalCoverage}
    />
  </div>

  <h2 id="source-formats" class="fr-mt-6w fr-mb-5w">Sources et formats</h2>

  <div class="form--content fr-mb-8w">
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

    <div
      class="fr-input-group fr-my-4w {$errors.technicalSource
        ? 'fr-input-group--error'
        : ''}"
    >
      <label class="fr-label" for="technicalSource">
        Système d'information source
        <span class="fr-hint-text" id="technicalSource-desc-hint">
          De quelle sources proviennent ces données ? Séparez leur nom par des
          “/” lorsqu'il y en a plusieurs.
        </span>
      </label>
      <input
        class="fr-input {$errors.technicalSource ? 'fr-input--error' : ''}"
        aria-describedby={$errors.technicalSource
          ? "technicalSource-desc-error"
          : null}
        type="text"
        id="technicalSource"
        name="technicalSource"
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={$form.technicalSource}
      />
      {#if $errors.technicalSource}
        <p id="technicalSource-desc-error" class="fr-error-text">
          {$errors.technicalSource}
        </p>
      {/if}
    </div>
  </div>
  <h2 id="mot-cles" class="fr-mb-5w">Mot-clés thématiques</h2>
  <div class="form--content fr-mb-8w">
    <div
      class={`fr-input-group fr-mt-8w ${
        hasTagsError ? "fr-input-group--error" : ""
      } `}
    >
      <label class="fr-label" for="tags">
        Mot-clés <RequiredMarker />
        <span class="fr-hint-text" id="tags-desc-hint">
          Les mot-clés seront utilisés par les réutilisateurs pour affiner leur
          recherche. Sélectionnez ceux qui vous semblent les plus représentatifs
          de vos données.
        </span>
      </label>

      <TagSelector
        selectedTags={initial.tags}
        on:change={handleTagsChange}
        name="tags"
        {tags}
      />

      {#if hasTagsError}
        <p id="tags-desc-error" class="fr-error-text">
          {$errors.tags}
        </p>
      {/if}
    </div>
  </div>

  <h2 id="contacts" class="fr-mt-6w fr-mb-5w">Contacts</h2>

  <p class="fr-mb-6w">
    Dans un soucis de traçabilité et de facilité de mise à jour, il est
    fondamental de pouvoir prendre contact avec l'organisation ou les personnes
    productrices d'une donnée. Lorsqu'une demande de contact sera effectuée,
    l'ensemble des adresses e-mail saisies recevront la notification.
  </p>

  <div class="form--content fr-mb-8w">
    <div
      class="fr-input-group fr-my-4w {$errors.producerEmail
        ? 'fr-input-group--error'
        : ''}"
    >
      <label class="fr-label" for="producerEmail">
        Adresse e-mail du service producteur
        <span class="fr-hint-text" id="producerEmail-desc-hint">
          Il est fortement conseillé d'avoir une adresse e-mail générique afin
          de rendre la prise de contact possible quelle que soit les personnes
          en responsabilité. Nous recommandons d'avoir une adresse différente
          pour chaque service afin de ne pas "polluer" les boîtes e-mail de
          chacun lorsque le catalogue grandit.
        </span>
      </label>
      <input
        class="fr-input {$errors.producerEmail ? 'fr-input--error' : ''}"
        aria-describedby={$errors.producerEmail
          ? "producerEmail-desc-error"
          : null}
        type="email"
        id="producerEmail"
        name="producerEmail"
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={$form.producerEmail}
      />
      {#if $errors.producerEmail}
        <p id="producerEmail-desc-error" class="fr-error-text">
          {$errors.producerEmail}
        </p>
      {/if}
    </div>

    <ContactEmailsField
      bind:errors={emailErrors}
      bind:contactEmails={$form.contactEmails}
      on:blur={handleChange}
      on:change={handleChange}
    />
  </div>

  <h2 id="mise-a-jour" class="fr-mt-6w fr-mb-5w">Mise à jour</h2>

  <p class="fr-mb-5w">
    A moins qu'il ne soit une production ponctuelle, un jeu de donnée n'est
    utile que lorsqu'il est à jour ! Avec ces quelques informations nous
    pourrons indiquer à vos réutilisateurs lorsque les données seront mises à
    jour.
  </p>

  <div class="form--content fr-mb-8w">
    <div
      class="fr-input-group fr-my-4w {$errors.lastUpdatedAt
        ? 'fr-input-group--error'
        : ''}"
    >
      <label class="fr-label" for="lastUpdatedAt">
        Date de la dernière mise à jour (JJ / MM / AAAA)
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
          on:change={handleLastUpdatedAtChange}
          on:blur={handleLastUpdatedAtChange}
          bind:value={$form.lastUpdatedAt}
        />

        {#if $errors.lastUpdatedAt}
          <p id="title-desc-error" class="fr-error-text">
            {$errors.lastUpdatedAt}
          </p>
        {/if}
      </div>
    </div>

    <Select
      options={toSelectOptions(UPDATE_FREQUENCY_LABELS)}
      id="updateFrequency"
      name="updateFrequency"
      placeholder="Sélectionner une option"
      label="Fréquence de mise à jour"
      bind:value={$form.updateFrequency}
      on:change={(event) =>
        handleSelectChange(
          "updateFrequency",
          event,
          handleChange,
          updateValidateField
        )}
      on:blur={(event) =>
        handleSelectChange(
          "updateFrequency",
          event,
          handleChange,
          updateValidateField
        )}
      error={$errors.updateFrequency}
    />
  </div>

  <h2 id="ouverture" class="fr-mt-6w fr-mb-5w">Ouverture</h2>

  <div class="form--content fr-mb-8w">
    <div
      class="fr-input-group fr-my-4w"
      class:fr-input-group--error={$errors.publishedUrl}
    >
      <label class="fr-label" for="publishedUrl">
        Page open data
        <span class="fr-hint-text" id="publishedUrl-desc-hint">
          Si le jeu de données est publié en open data, saisissez ici le lien de
          la page web associée.
        </span>
      </label>

      <input
        class="fr-input"
        class:fr-input--error={$errors.lastUpdatedAt}
        aria-describedby={$errors.publishedUrl
          ? "publishedUrl-desc-error"
          : null}
        type="text"
        id="publishedUrl"
        name="publishedUrl"
        on:change={handleChange}
        on:blur={handleChange}
        bind:value={$form.publishedUrl}
      />

      {#if $errors.publishedUrl}
        <p id="publishedUrl-desc-error" class="fr-error-text">
          {$errors.publishedUrl}
        </p>
      {/if}
    </div>
  </div>

  <div class="fr-input-group button--container fr-mb-6w">
    <button
      type="submit"
      class="fr-btn  fr-fi-upload-2-line fr-btn--icon-right"
    >
      {saveBtnLabel}
    </button>
  </div>
</form>

<style>
  textarea {
    resize: vertical;
  }

  .button--container {
    display: flex;
    justify-content: flex-end;
  }

  .form--content {
    width: 80%;
    padding: auto;
    margin: auto;
  }
</style>
