export type InputEvent = Event & {
  currentTarget: EventTarget & HTMLInputElement & { currentValue: string };
};
export type OptionEvent = Event & {
  currentTarget: EventTarget & HTMLOptionElement;
};
