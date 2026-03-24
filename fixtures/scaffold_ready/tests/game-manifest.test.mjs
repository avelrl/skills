import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const manifestPath = resolve(process.cwd(), "data/game-manifest.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));

test("game manifest is aligned with the designed first system", () => {
  assert.equal(manifest.id, "courier-drift");
  assert.equal(manifest.targetSystem, "Player Movement");
  assert.equal(manifest.buildGoal, "Scaffold only");
  assert.ok(Array.isArray(manifest.todo));
  assert.ok(manifest.todo.length >= 3);
});
