import { get } from "svelte/store";
import type { LoadOutput } from "@sveltejs/kit";
import { isLoggedIn, user } from "../stores/auth";
import { checkLogin } from "../repositories/auth";
import { PUBLIC_PAGES } from "src/constants";

let lastAuthCheckTime = 0;
const AUTH_CHECK_PERIOD_SECONDS = 30 * 1000;

/**
 * Force-redirect to the login page if an unauthenticated user
 * is attempting to access a protected page.
 */
export const authGuard = async (url: URL): Promise<LoadOutput> => {
  if (PUBLIC_PAGES.includes(url.pathname)) {
    return {};
  }

  if (!get(isLoggedIn)) {
    return {
      status: 302,
      redirect: "/login",
    };
  }

  // We have auth state stored in the browser... But is the user session still valid?
  // Maybe the user got deleted, their tokens has changed. Who knows?
  //
  // In SvelteKit, the easiest solution is a session cookie set by the server in a SvelteKit endpoint.
  // But we have an external API, perhaps on a different domain -- so cookies are more complex to use.
  // We use a simpler mechanism: poll the API for auth validity every now and then upon navigation.
  //
  // Note that we would redirect if we get a 401 Unauthorized from the API during an API call too.
  // So this is just an extra login check.

  const shouldCheckAuth =
    Date.now() - lastAuthCheckTime > AUTH_CHECK_PERIOD_SECONDS;

  if (!shouldCheckAuth) {
    return {};
  }

  const { status } = await checkLogin({ fetch, apiToken: get(user).apiToken });
  const isAuthenticated = status === 200;
  lastAuthCheckTime = Date.now();

  if (!isAuthenticated) {
    return {
      status: 302,
      redirect: "/login",
    };
  }

  return {};
};
