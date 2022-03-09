import "@testing-library/jest-dom";

import index from "./index.svelte";
import { render, fireEvent } from "@testing-library/svelte";

const dataset = {
  id: "d4765f06-ccdf-4bae-b237-2bced67e6dc2",
  title: "foo",
  description: "bar baz crux",
  formats: ["other"],
};

describe("Test the dataset detail page header", () => {
  test("The dataset title is present", () => {
    const { getByRole } = render(index, { dataset });
    expect(getByRole("heading", { level: 1 })).toHaveTextContent(dataset.title);
  });
});

describe("Test the dataset detail page action buttons", () => {
  test("The button to modify the dataset is present", () => {
    const { getByText } = render(index, { dataset });
    const modifyButton = getByText("Proposer une modification");
    expect(modifyButton).toBeInTheDocument();
    expect(modifyButton.getAttribute("href")).toContain(dataset.id);
  });
  test("The button to contact the author is present", () => {
    const { getByText } = render(index, { dataset });
    expect(getByText("Contacter le producteur")).toBeInTheDocument();
  });
  test("The button to follow the dataset is present", () => {
    const { getByText } = render(index, { dataset });
    expect(getByText("Suivre")).toBeInTheDocument();
  });
});

describe("Test the dataset detail page tabs", () => {
  test("The tabs are present", () => {
    const { getAllByRole } = render(index, { dataset });
    const tabs = getAllByRole("tab");
    expect(tabs.length).toEqual(4);
    expect(tabs[0]).toHaveTextContent("Résumé");
    expect(tabs[1]).toHaveTextContent("Sources");
    expect(tabs[2]).toHaveTextContent("Contenu");
    expect(tabs[3]).toHaveTextContent("Discussion");
  });
  test("The 'Résumé' tab panels displays the description", async () => {
    const { getAllByRole } = render(index, { dataset });
    const panel = getAllByRole("tabpanel")[0];
    expect(panel).toHaveTextContent(dataset.description);
  });
});