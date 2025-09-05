/**
 * Utility functions for converting between camelCase and snake_case
 * Used for converting between frontend (camelCase) and backend (snake_case) naming conventions
 */

/**
 * Converts a snake_case string to camelCase
 * @param str - The snake_case string to convert
 * @returns The camelCase version of the string
 */
export function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (g) => g[1].toUpperCase());
}

/**
 * Converts a camelCase string to snake_case
 * @param str - The camelCase string to convert
 * @returns The snake_case version of the string
 */
export function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

/**
 * Recursively converts all keys in an object using the provided converter function
 * @param obj - The object to convert
 * @param converter - The function to use for key conversion
 * @returns A new object with converted keys
 */
export function convertKeys<T extends object>(
  obj: T,
  converter: (str: string) => string
): any {
  if (Array.isArray(obj)) {
    return obj.map((item) => convertKeys(item, converter));
  }

  if (typeof obj !== 'object' || obj === null) {
    return obj;
  }

  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => [
      converter(key),
      typeof value === 'object' ? convertKeys(value, converter) : value,
    ])
  );
}

/**
 * Converts all keys in an object from camelCase to snake_case
 * @param obj - The object to convert
 * @returns A new object with snake_case keys
 */
export const toSnakeCaseKeys = <T extends object>(obj: T) =>
  convertKeys(obj, toSnakeCase);

/**
 * Converts all keys in an object from snake_case to camelCase
 * @param obj - The object to convert
 * @returns A new object with camelCase keys
 */
export const toCamelCaseKeys = <T extends object>(obj: T) =>
  convertKeys(obj, toCamelCase);