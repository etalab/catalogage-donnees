import type {
  LoginApiRequestData,
  LoginApiResponseData,
} from "src/definitions/auth";
import type { ApiResponse, Fetch } from "src/definitions/fetch";
import { getApiUrl, getHeaders } from "../fetch";

type Login = (opts: {
  fetch: Fetch;
  data: LoginApiRequestData;
}) => Promise<ApiResponse<LoginApiResponseData>>;

export const login: Login = async ({ fetch, data }) => {
  const body = JSON.stringify(data);
  const url = `${getApiUrl()}/auth/login/`;

  const request = new Request(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });

  const response = await fetch(request);

  const apiData = await response.json();

  return {
    status: response.status,
    data: {
      email: apiData.email,
      role: apiData.role,
      apiToken: apiData.api_token,
    },
  };
};

type CheckLogin = (opts: {
  fetch: Fetch;
  apiToken: string;
}) => Promise<ApiResponse<void>>;

export const checkLogin: CheckLogin = async ({ fetch, apiToken }) => {
  const url = `${getApiUrl()}/auth/check/`;
  const request = new Request(url, { headers: getHeaders(apiToken) });
  const response = await fetch(request);
  return {
    status: response.status,
  };
};
