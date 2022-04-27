import type { Tag } from "src/definitions/tag";

export const buildFakeTag = (tag: Partial<Tag> = {}): Tag => {
  return {
    id: tag.id || "uuid",
    name: tag.name || "my-tag",
  };
};
