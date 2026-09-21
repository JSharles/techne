import { test } from "node:test";
import assert from "node:assert/strict";
import { allWithin, hasDuplicate } from "./duplicates.ts";

test("finds a repeated value", () => assert.equal(hasDuplicate([1, 2, 3, 1]), true));
test("reports no repeat when every value is distinct", () => assert.equal(hasDuplicate([1, 2, 3]), false));
test("finds no repeat in an empty array", () => assert.equal(hasDuplicate([]), false));
test("accepts values inside the bounds, bounds included", () => assert.equal(allWithin([1, 5, 10], 1, 10), true));
test("rejects a value outside the bounds", () => assert.equal(allWithin([1, 11], 1, 10), false));
test("accepts an empty array", () => assert.equal(allWithin([], 1, 10), true));
