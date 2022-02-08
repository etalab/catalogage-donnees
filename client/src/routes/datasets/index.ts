import type { RequestHandler } from "@sveltejs/kit";
import { api } from "./_api";

export const get: RequestHandler = async ({ request }) => {
  return await api(request, "/datasets/");
};

export const post: RequestHandler = async ({ request }) => {
  const form = await request.formData();
  return api(request, "/datasets/", {
    title: form.get("title"),
    description: form.get("description"),
  });
};

export const put: RequestHandler = async ({ request }) => {
  const form = await request.formData();
  return api(request, `/datasets/${form.get("id")}/`, {
    title: form.get("title"),
    description: form.get("description"),
  });
};

export const del: RequestHandler = async ({ request }) => {
  const form = await request.formData();
  return api(request, `/datasets/${form.get("id")}/`);
};
