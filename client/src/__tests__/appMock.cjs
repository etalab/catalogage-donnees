// Used by Jest to resolve contents of "$app/*" imports.
// NOTE: this is a dirty hack around some issues with Svelte/Vite/Jest integration.
// See: https://github.com/etalab/catalogage-donnees/pull/48#discussion_r797566212
// See: https://github.com/rossyman/svelte-add-jest/issues/12
// See: https://github.com/rossyman/svelte-add-jest/issues/14
module.exports = {
  browser: false,
}
