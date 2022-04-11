import { getFakeDataSet } from "src/fixtures/dataset";
import { toDataset, toPayload } from "./dataset";

describe("transformers -- dataset", () => {
  describe("toPayload", () => {
    const dataset = getFakeDataSet({});
    const result = toPayload(dataset);
    const keys = Object.keys(result);
    [
      "entrypoint_email",
      "contact_emails",
      "first_published_at",
      "update_frequency",
      "last_updated_at",
    ].forEach((item) => {
      expect(keys).toContain(item);
    });
  });

  describe("toDataset", () => {
    const dataset = toPayload(getFakeDataSet({}));
    const result = toDataset(dataset);
    const keys = Object.keys(result);
    ["entrypointEmail", "contactEmails", "updateFrequency"].forEach((item) => {
      expect(keys).toContain(item);
    });
  });
});
