import type { SelectOption } from "src/definitions/form";

export const toSelectOptions = (labelsMap: {
  [key: string]: any;
}): Array<SelectOption> => {
  return Object.keys(labelsMap).map((item, index) => ({
    id: `${labelsMap[item]}-${index}`,
    label: labelsMap[item],
    value: item,
  }));
};
