import type { UserInfo, User } from "src/definitions/auth";
import { derived } from "svelte/store";
import { Maybe } from "$lib/util/maybe";
import { storable } from "../localStorage";

const validateExistingUserInfo = (value: UserInfo): boolean => {
  const { loggedIn, user } = value;
  return (loggedIn && !!user) || (!loggedIn && !user);
};

const userInfo = storable<UserInfo>(
  "user-info",
  { loggedIn: false, user: null },
  validateExistingUserInfo
);

export const user = derived(userInfo, (values) => values.user);

export const apiToken = derived(user, ($user) => {
  return Maybe.Some($user) ? $user.apiToken : "";
});

export const isAdmin = derived(user, (user) => {
  return user?.role === "ADMIN";
});

export const login = (user: User): void => {
  userInfo.set({ loggedIn: true, user });
};

export const logout = (): void => {
  userInfo.set({ loggedIn: false, user: null });
};
