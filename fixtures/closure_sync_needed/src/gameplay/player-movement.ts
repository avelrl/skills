import { PLAYER_SPAWN, WORLD_BOUNDS } from "./config";
import { add, moveInsideBounds, normalize, scale, vec } from "./shared";
import type { Bounds, InputState, PlayerState } from "./types";

const ATTACK_COOLDOWN = 0.44;
const ATTACK_DURATION = 0.16;
const ATTACK_SURGE_SPEED = 180;

export function createPlayer(): PlayerState {
  return {
    position: { ...PLAYER_SPAWN },
    velocity: vec(0, 0),
    facing: vec(1, 0),
    radius: 16,
    speed: 250,
    health: 4,
    maxHealth: 4,
    attackCooldown: 0,
    attackTimer: 0,
    attackId: 0,
    invulnerabilityTimer: 0
  };
}

export function updatePlayerMovement(
  player: PlayerState,
  input: InputState,
  deltaSeconds: number,
  bounds: Bounds = WORLD_BOUNDS
): void {
  player.attackCooldown = Math.max(0, player.attackCooldown - deltaSeconds);
  player.attackTimer = Math.max(0, player.attackTimer - deltaSeconds);
  player.invulnerabilityTimer = Math.max(
    0,
    player.invulnerabilityTimer - deltaSeconds
  );

  const desiredDirection = normalize(
    vec(
      (input.right ? 1 : 0) - (input.left ? 1 : 0),
      (input.down ? 1 : 0) - (input.up ? 1 : 0)
    )
  );

  if (desiredDirection.x !== 0 || desiredDirection.y !== 0) {
    player.facing = desiredDirection;
  }

  if (input.attackPressed && player.attackCooldown <= 0) {
    player.attackCooldown = ATTACK_COOLDOWN;
    player.attackTimer = ATTACK_DURATION;
    player.attackId += 1;
  }

  const moveSpeed = player.attackTimer > 0 ? player.speed * 0.62 : player.speed;
  let velocity = scale(desiredDirection, moveSpeed);

  if (player.attackTimer > 0) {
    velocity = add(velocity, scale(player.facing, ATTACK_SURGE_SPEED));
  }

  player.velocity = velocity;
  player.position = moveInsideBounds(
    add(player.position, scale(player.velocity, deltaSeconds)),
    player.radius,
    bounds
  );
}

export function damagePlayer(player: PlayerState): void {
  if (player.invulnerabilityTimer > 0) {
    return;
  }

  player.health = Math.max(0, player.health - 1);
  player.invulnerabilityTimer = 1;
}
