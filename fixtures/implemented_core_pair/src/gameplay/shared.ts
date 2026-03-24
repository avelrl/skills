import type { Bounds, Vector2 } from "./types";

export const TAU = Math.PI * 2;

export function vec(x: number, y: number): Vector2 {
  return { x, y };
}

export function add(a: Vector2, b: Vector2): Vector2 {
  return { x: a.x + b.x, y: a.y + b.y };
}

export function subtract(a: Vector2, b: Vector2): Vector2 {
  return { x: a.x - b.x, y: a.y - b.y };
}

export function scale(vector: Vector2, amount: number): Vector2 {
  return { x: vector.x * amount, y: vector.y * amount };
}

export function dot(a: Vector2, b: Vector2): number {
  return a.x * b.x + a.y * b.y;
}

export function length(vector: Vector2): number {
  return Math.hypot(vector.x, vector.y);
}

export function normalize(vector: Vector2): Vector2 {
  const magnitude = length(vector);

  if (magnitude === 0) {
    return { x: 0, y: 0 };
  }

  return {
    x: vector.x / magnitude,
    y: vector.y / magnitude
  };
}

export function distance(a: Vector2, b: Vector2): number {
  return length(subtract(a, b));
}

export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

export function moveInsideBounds(
  position: Vector2,
  radius: number,
  bounds: Bounds
): Vector2 {
  return {
    x: clamp(position.x, radius, bounds.width - radius),
    y: clamp(position.y, radius, bounds.height - radius)
  };
}
