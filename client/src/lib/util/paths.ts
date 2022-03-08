// Simplified implementation of: https://github.com/garybernhardt/static-path
// Credits: https://www.youtube.com/watch?v=KRMJIiGE0ds

/**
 * In:  '/items/:itemId/objects/:objectId'
 * Out: 'itemId' | 'lessonId'
 */
type PathParamNames<Pattern extends string> =
  // prettier-ignore
  Pattern extends `:${infer Param}/${infer Rest}` ? Param | PathParamNames<Rest>
  : Pattern extends `:${infer Param}` ? Param
  : Pattern extends `${infer _Prefix}:${infer Rest}` ? PathParamNames<`:${Rest}`>
  : never;

/**
 * In:  '/items/:itemId'
 * Out: { itemId: string }
 */
type Params<Pattern extends string> =
  // prettier-ignore
  string extends Pattern ? never
  : { [K in PathParamNames<Pattern>]: string };

type Part<Pattern extends string> =
  | { type: "constant"; value: string }
  | { type: "param"; paramName: PathParamNames<Pattern> };

export type Path<Pattern extends string> = (params: Params<Pattern>) => string;

/**
 * Represent a path in a type-safe manner.
 *
 * Usage:
 *
 * const itemDetail = path('/items/:itemId');
 * const href = itemDetail({ itemId: '...' });
 */
export const path = <Pattern extends string>(
  pattern: Pattern
): Path<Pattern> => {
  const parts = makePatternParts(pattern);

  return (params: Params<Pattern>) => {
    const pathValues = parts
      .map((part) => {
        if (part.type === "param") {
          return getParamValue(params, part.paramName);
        }
        return part.value;
      })
      .filter(
        // Drop any leading empty part,
        // since we add the leading / manually on the next line
        (value, index) => (index === 0 ? value !== "" : true)
      );
    return `/${pathValues.join("/")}`;
  };
};

/**
 * Split a pattern into structured parts.
 */
const makePatternParts = <Pattern extends string>(
  pattern: Pattern
): Part<Pattern>[] => {
  return pattern.split("/").map((value) => {
    if (value.startsWith(":")) {
      return {
        type: "param",
        paramName: value.replace(/^:/, "") as PathParamNames<Pattern>,
      };
    }
    return { type: "constant", value };
  });
};

const getParamValue = <Pattern extends string>(
  params: Params<Pattern>,
  paramName: keyof Params<Pattern>
): string => {
  const value = params[paramName];
  if (typeof value !== "string") {
    const formattedParam = JSON.stringify({ paramName });
    throw new Error(
      `When generating a path, param ${formattedParam} did not exist on params object. ` +
        "Types should have prevented this, so either you bypassed type checks, or there is a bug!"
    );
  }
  return value;
};
