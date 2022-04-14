import { getFakeDataset } from "src/tests/factories/dataset";
import {
  toDataset,
  toPayload,
  camelToUnderscore,
  transformKeysToUnderscoreCase,
} from "./dataset";

describe("transformers -- dataset", () => {
  test("transformKeysToUnderscoreCase", () => {
    const text = "helloWorld";
    const result = camelToUnderscore(text);
    expect(result).toBe("hello_world");
  });

  test("transformKeysToUnderscoreCase", () => {
    const input = {
      helloWorld: "hello",
      fooBaz: "hello",
    };
    const result = transformKeysToUnderscoreCase(input);

    expect(Object.keys(result).every((key) => key.includes("_"))).toBe(true);
  });

  test("toPayload", () => {
    const dataset = getFakeDataset();
    const result = toPayload(dataset);
    expect(Object.keys(result).every((key) => key === key.toLowerCase())).toBe(
      true
    );
  });

  test("toDataset", () => {
    const dataset = toPayload(getFakeDataset());
    const result = toDataset(dataset);
    expect(Object.keys(result).every((key) => key === key.toLowerCase())).toBe(
      false
    );
  });
});
