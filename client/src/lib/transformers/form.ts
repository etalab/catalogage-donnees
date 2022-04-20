import type { SelectOption } from "src/definitions/form";

export const toSelectOptions = (labelsMap: {
  [key: string]: string;
}): Array<SelectOption> => {
  return Object.keys(labelsMap).map(
    (item): SelectOption => ({
      label: labelsMap[item],
      value: item,
    })
  );
};
