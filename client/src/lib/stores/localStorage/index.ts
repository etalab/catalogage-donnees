import { writable } from "svelte/store";
import type { Writable } from "svelte/store";

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
  initialValue: T
): Writable<T> => {
  const store = writable(initialValue);

  const existingValue = getFromLocalStorage<T>(key);

  if (existingValue) {
    store.set(existingValue);
  } else {
    persistToLocalStorage(key, initialValue);
  }

  store.subscribe((value) => {
    persistToLocalStorage(key, value);
  });

  return store;
};
