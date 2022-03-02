import type { UserInfo } from "src/definitions/auth";
import { derived } from "svelte/store";
import { storable } from "../localStorage";

const userInfo = storable<UserInfo>("user-info", { loggedIn: false });

export const isLoggedIn = derived(userInfo, (values) => values.loggedIn);

export const login = () => {
  userInfo.set({ loggedIn: true });
};

export const logout = () => {
  userInfo.set({ loggedIn: false });
};
