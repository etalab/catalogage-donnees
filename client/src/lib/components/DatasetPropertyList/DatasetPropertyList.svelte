<script lang="ts">
  type Property = {
    label: string;
    icon: string;
    value: string;
  };

  export let properties: Property[];
</script>

<div class="property-list fr-row">
  {#each properties as { icon, label, value }}
    <div class="property-list-item fr-col-{Math.floor(12 / properties.length)}">
      <span class={icon} aria-hidden="true" />

      <div class="fr-text--xs fr-my-0 fr-ml-1w">
        <div class="fr-text-mention--grey">
          {label}
        </div>
        <div>
          {value}
        </div>
      </div>
    </div>
  {/each}
</div>

<style>
  .property-list {
    display: flex;
    gap: var(--sp-2w);
  }

  .property-list-item {
    display: flex;
    align-items: center;
  }

  [class*="fr-icon"] {
    color: var(--text-action-high-blue-france);
    margin-top: 0.2rem; /* Adjust vertical alignment */
  }
</style>
