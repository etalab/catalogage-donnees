import type { Fetch } from "src/definitions/fetch";
import { login } from "./auth";

test("The login endpoint behaves as expected", async () => {
  const fakeToken = "abcd1234";
  const email = "fake@example.org";
  const password = "p@ssw0rd";
  const data = { email, password };

  const fakeFetch: Fetch = async (request) => {
    expect(request.method).toBe("POST");
    expect(new URL(request.url, "http://test").pathname).toBe("/auth/login/");
    expect(JSON.parse(await request.text())).toEqual(data);
    const body = JSON.stringify({ email, api_token: fakeToken });
    const headers = { "Content-Type": "application/json" };
    return new Response(body, { headers, status: 201 });
  };

  const response = await login({ fetch: fakeFetch, data });

  expect(response.status).toBe(201);
  expect(response.data).toEqual({ email, apiToken: fakeToken });
});
