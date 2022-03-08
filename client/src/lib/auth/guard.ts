import { get } from "svelte/store";
import type { LoadOutput } from "@sveltejs/kit";
import { browser } from "$app/env";
import { isLoggedIn } from "../stores/auth";

const isPublicPage = (url: URL): boolean => {
  return url.pathname === "/login";
};

/**
 * Force-redirect to the login page if an unauthenticated user
 * is attempting to access a protected page.
 */
export const authGuard = (url: URL): LoadOutput => {
  if (isPublicPage(url)) {
    return {};
  }

  if (!browser) {
    return {};
  }

  if (get(isLoggedIn)) {
    return {};
  }

  return {
    status: 302,
    redirect: "/login",
  };
};
