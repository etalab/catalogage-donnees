export interface LoginFormData {
  email: string;
  password: string;
}

export interface LoginApiRequestData {
  email: string;
  password: string;
}

export interface LoginApiResponseData {
  email: string;
  apiToken: string;
}

export interface User {
  email: string;
  apiToken: string;
}

export interface UserInfo {
  loggedIn: boolean;
  user: User | null;
}
