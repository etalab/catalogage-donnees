<script lang="ts">
  export let icon: string;
</script>

<div class="property-item">
  <span class="fr-fi {icon}" aria-hidden="true" />

  <div class="fr-text--xs fr-my-0 fr-ml-1w">
    <div class="fr-text-mention--grey">
      <slot name="label" />
    </div>
    <div>
      <slot name="value" />
    </div>
  </div>
</div>

<style>
  .property-item {
    display: flex;
    align-items: center;
  }

  [class*="fr-fi"] {
    color: var(--text-action-high-blue-france);
    margin-top: 0.2rem; /* Adjust vertical alignment */
  }
</style>
