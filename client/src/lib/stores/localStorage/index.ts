import { writable, get } from "svelte/store";
import type { Writable, Updater } from "svelte/store";

const hasLocalStorage = typeof localStorage !== "undefined";

const getFromLocalStorage = <T = unknown>(key: string): T | null => {
  if (!hasLocalStorage) {
    return null;
  }

  const rawValue = localStorage.getItem(key) || "null";

  return JSON.parse(rawValue) as T;
};

const persistToLocalStorage = <T = unknown>(key: string, value: T) => {
  if (!hasLocalStorage) {
    return;
  }

  if (!value) {
    return;
  }

  // XXX: RGPD? Cookie consent?
  const encodedValue = JSON.stringify(value);
  localStorage.setItem(key, encodedValue);
};

/**
 * Return a writable store that persists its value to localStorage.
 */
export const storable = <T = unknown>(
  key: string,
  initialValue: T,
  validateExisting: (value: T) => boolean = (value) => true,
): Writable<T> => {
  const store = writable(initialValue);

  const existingValue = getFromLocalStorage<T>(key);

  if (existingValue && validateExisting(existingValue)) {
    store.set(existingValue);
  } else {
    persistToLocalStorage(key, initialValue);
  }

  const wrappedStore = {
    set(value: T) {
      persistToLocalStorage(key, value);
      store.set(value);
    },
    update(updater: Updater<T>) {
      this.set(updater(get(store)));
    },
    subscribe: store.subscribe.bind(store),
  };

  return wrappedStore;
};
