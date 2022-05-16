/**
 * @jest-environment jsdom
 */
import "@testing-library/jest-dom";
import { render, fireEvent } from "@testing-library/svelte";
import type { LoginFormData } from "src/definitions/auth";

import LoginForm from "./LoginForm.svelte";

describe("Test the dataset list item", () => {
  test("The 'email' field is present", () => {
    const { getByLabelText } = render(LoginForm);
    const email = getByLabelText("Adresse e-mail");
    expect(email).toBeInTheDocument();
    expect(email).toHaveAttribute("type", "email");
  });

  test("The 'password' field is present", () => {
    const { getByLabelText } = render(LoginForm);
    const password = getByLabelText("Mot de passe");
    expect(password).toBeInTheDocument();
    expect(password).toHaveAttribute("type", "password");
  });

  test("The 'submit' button is present", () => {
    const { getByRole } = render(LoginForm);
    expect(getByRole("button")).toBeInTheDocument();
  });

  test("The 'submit' button displays a loading text when loading", async () => {
    const { getByRole, rerender } = render(LoginForm);
    let button = getByRole("button");
    expect(button).toHaveTextContent("Se connecter");

    rerender({ props: { loading: true } });
    button = getByRole("button");
    expect(button).toHaveTextContent("Connexion en cours...");
  });

  test("The form displays an error text when login failed", async () => {
    const { queryByText, getByText, rerender } = render(LoginForm);
    let error = queryByText("Adresse e-mail ou identifiant invalide");
    expect(error).not.toBeInTheDocument();

    rerender({ props: { loginFailed: true } });
    error = getByText("Adresse e-mail ou identifiant invalide");
    expect(error).toBeInTheDocument();
  });

  test("The form submits the logged in user", async () => {
    const { getByRole, getByLabelText, component } = render(LoginForm);

    await fireEvent.input(getByLabelText("Adresse e-mail"), {
      target: { value: "user@mydomain.org" },
    });
    await fireEvent.input(getByLabelText("Mot de passe"), {
      target: { value: "p@ssw0rd" },
    });
    await fireEvent.click(getByRole("button"));

    const submittedValue = await new Promise<LoginFormData>((resolve) => {
      component.$on("submit", (event) => resolve(event.detail));
    });

    expect(submittedValue).toEqual({
      email: "user@mydomain.org",
      password: "p@ssw0rd",
    });
  });
});
