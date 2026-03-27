import type { Bounds, Vector2 } from "./types";

export const WORLD_BOUNDS: Bounds = {
  width: 960,
  height: 540
};

export const PLAYER_SPAWN: Vector2 = {
  x: 140,
  y: 405
};

export const ENEMY_SPAWN: Vector2 = {
  x: 610,
  y: 228
};

export const RELAY_GATE: Vector2 = {
  x: 822,
  y: 118
};

export const RELAY_GATE_RADIUS = 42;
export const DELIVERY_DEADLINE = 40;
