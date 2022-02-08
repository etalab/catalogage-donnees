import { getApiUrl } from "src/lib/fetch";

export async function api(
  request: Request,
  resource: string,
  data?: Record<string, unknown>
) {
  const res = await fetch(`${getApiUrl()}${resource}`, {
    method: request.method,
    headers: {
      "content-type": "application/json",
    },
    body: data && JSON.stringify(data),
  });

  // If this is a <form> submission, be sure to redirect to the client page,
  // rather than letting the browser show the `action` URL (which points to the API result).
  if (
    res.ok &&
    request.method !== "GET" &&
    request.headers.get("accept") != "application/json"
  ) {
    return {
      status: 303,
      headers: {
        location: "/",
      },
    };
  }

  return {
    status: res.status,
    body: await res.json(),
  };
}
