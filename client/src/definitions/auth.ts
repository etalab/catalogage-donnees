export interface LoginFormData {
  email: string;
  password: string;
}

export interface LoginApiRequestData {
  email: string;
  password: string;
}

export interface LoginApiResponseData {
  apiToken: string;
}

export interface UserInfo {
  loggedIn: boolean;
}
