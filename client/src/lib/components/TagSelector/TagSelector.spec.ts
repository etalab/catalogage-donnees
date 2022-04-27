import "@testing-library/jest-dom";

import TagSelector from "./TagSelector.svelte";
import { render, fireEvent } from "@testing-library/svelte";

describe("Test the TagSelector", () => {
  test("should display no selected tags", async () => {
    const { queryAllByRole } = render(TagSelector, {
      name: "my-list",
      selectedTags: [],
      tags: [
        {
          id: 1,
          name: "foo",
        },
        {
          id: 2,
          name: "toto",
        },
      ],
    });

    expect(queryAllByRole("listitem")).toHaveLength(0);
  });

  test("should select and display a tag", async () => {
    const { getByRole, getAllByRole } = render(TagSelector, {
      name: "my-list",
      selectedTags: [],
      tags: [
        {
          id: "uuid1",
          name: "foo",
        },
        {
          id: "uuid2",
          name: "toto",
        },
      ],
    });

    const input = getByRole("search");

    await fireEvent.input(input, {
      target: {
        value: "toto",
      },
    });

    const tags = getAllByRole("listitem");
    expect(tags).toHaveLength(1);
    const tag = tags[0];
    expect(tag).toHaveTextContent("toto");
  });

  test("should remove one tag from tag list", async () => {
    const { getByRole, getAllByRole, queryAllByRole } = render(TagSelector, {
      name: "my-list",
      selectedTags: [],
      tags: [
        {
          id: "uuid1",
          name: "foo",
        },
        {
          id: "uuid2",
          name: "toto",
        },
      ],
    });

    const input = getByRole("search");

    await fireEvent.input(input, {
      target: {
        value: "toto",
      },
    });

    let tags = getAllByRole("listitem");
    const tag = tags[0];

    await fireEvent.click(tag);

    tags = queryAllByRole("listitem");
    expect(tags).toHaveLength(0);
  });

  test("should display one selected tag", async () => {
    const { getAllByRole } = render(TagSelector, {
      name: "my-list",
      selectedTags: [
        {
          id: "uuid",
          name: "toto",
        },
      ],
      tags: [
        {
          id: "uuid",
          name: "toto",
        },
      ],
    });

    const tags = getAllByRole("listitem");
    expect(tags).toHaveLength(1);
  });
});
