<script context="module" lang="ts">
  export const prerender = true;
</script>

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

  const { form, errors, handleChange, handleSubmit, isSubmitting } = createForm(
    {
      initialValues: {
        name: "",
      },
      validationSchema: yup.object().shape({
        name: yup.string().required(),
      }),
      onSubmit: (values) => {
        const result = postData(values);
        console.log(result);
        return result;
      },
    }
  );
</script>

<section>
  <form on:submit={handleSubmit}>
    <label for="name">Name</label>
    <input
      id="name"
      name="name"
      on:change={handleChange}
      on:blur={handleChange}
      bind:value={$form.name}
    />
    {#if $errors.name}
      <small>{$errors.name}</small>
    {/if}

    <button type="submit">
      {#if $isSubmitting}loading...{:else}submit{/if}
    </button>
  </form>
</section>
