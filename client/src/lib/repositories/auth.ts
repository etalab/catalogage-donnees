import type {
  LoginApiRequestData,
  LoginApiResponseData,
} from "src/definitions/auth";
import type { ApiResponse, Fetch } from "src/definitions/fetch";
import { getApiUrl } from "../fetch";

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
      apiToken: apiData.api_token,
    },
  };
};
