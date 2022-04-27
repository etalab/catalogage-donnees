export const omit = (
  obj: { [key: string]: unknown },
  props: string[]
): { [key: string]: unknown } => {
  const temp = { ...obj };
  props.forEach((prop) => delete temp[prop]);
  return temp;
};
