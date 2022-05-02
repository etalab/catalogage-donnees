import { writable } from "svelte/store";
import type { Maybe } from "src/lib/util/maybe";

type ApiError = {
  status: number;
  detail: string;
};

export const apiErrors = writable<Maybe<ApiError>>();

export const pushApiError = async (response: Response): Promise<void> => {
  let detail: string;

  try {
    detail = (await response.json()).detail;
  } catch {
    detail = response.statusText;
  }

  apiErrors.set({ status: response.status, detail });
};
