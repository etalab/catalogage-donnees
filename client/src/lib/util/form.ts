export const handleSelectChange = async <Inf>(
  fieldname: keyof Inf,
  event: Event,
  handleChange: (event: Event) => Promise<void>,
  updateValidateField: (fieldname: keyof Inf, event: Event) => void
): Promise<void> => {
  const target = event.currentTarget as EventTarget & HTMLSelectElement;

  if (target.value === "null" || !target.value) {
    // Empty option selected.
    // Needs manual handling to ensure a `null` initial value and the empty
    // option all correspond to `null`.
    updateValidateField(fieldname, null);
    return;
  }

  await handleChange(event);
};
