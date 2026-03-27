import { ENEMY_SPAWN, WORLD_BOUNDS } from "./config";
import {
  add,
  distance,
  dot,
  moveInsideBounds,
  normalize,
  scale,
  subtract,
  vec
} from "./shared";
import { damagePlayer } from "./player-movement";
import type { CombatEvents, EnemyState, PlayerState, Vector2 } from "./types";

const TELEGRAPH_DURATION = 0.8;
const STRIKE_DURATION = 0.24;
const RECOVER_DURATION = 0.65;

function pushEnemyFromHit(enemy: EnemyState, player: PlayerState): void {
  const retreat = normalize(subtract(enemy.position, player.position));
  enemy.position = moveInsideBounds(
    add(enemy.position, scale(retreat, 20)),
    enemy.radius,
    WORLD_BOUNDS
  );
}

function canPlayerHitEnemy(player: PlayerState, enemy: EnemyState): boolean {
  const toEnemy = subtract(enemy.position, player.position);
  const facing = normalize(player.facing);
  const enemyDirection = normalize(toEnemy);
  const reach = distance(player.position, enemy.position);

  return reach <= 78 && dot(facing, enemyDirection) >= 0.3;
}

function startTelegraph(enemy: EnemyState, targetDirection: Vector2): void {
  enemy.phase = "telegraph";
  enemy.phaseTimer = TELEGRAPH_DURATION;
  enemy.strikeDirection = targetDirection;
  enemy.velocity = vec(0, 0);
  enemy.hitPlayerThisStrike = false;
}

function startStrike(enemy: EnemyState): void {
  enemy.phase = "strike";
  enemy.phaseTimer = STRIKE_DURATION;
}

function startRecover(enemy: EnemyState): void {
  enemy.phase = "recover";
  enemy.phaseTimer = RECOVER_DURATION;
  enemy.velocity = vec(0, 0);
}

export function createEnemy(): EnemyState {
  return {
    position: { ...ENEMY_SPAWN },
    velocity: vec(0, 0),
    radius: 18,
    speed: 118,
    health: 3,
    maxHealth: 3,
    phase: "chase",
    phaseTimer: 1.1,
    strikeDirection: vec(-1, 0),
    hitPlayerThisStrike: false,
    lastRegisteredAttackId: -1,
    defeated: false
  };
}

export function updateCombatLoop(
  player: PlayerState,
  enemy: EnemyState,
  deltaSeconds: number
): CombatEvents {
  const events: CombatEvents = {
    playerDamaged: false,
    enemyDamaged: false,
    enemyDefeated: false
  };

  if (!enemy.defeated && player.attackTimer > 0) {
    if (
      enemy.lastRegisteredAttackId !== player.attackId &&
      canPlayerHitEnemy(player, enemy)
    ) {
      enemy.lastRegisteredAttackId = player.attackId;
      enemy.health = Math.max(0, enemy.health - 1);
      pushEnemyFromHit(enemy, player);
      events.enemyDamaged = true;

      if (enemy.health <= 0) {
        enemy.defeated = true;
        enemy.phase = "down";
        enemy.phaseTimer = 0;
        enemy.velocity = vec(0, 0);
        events.enemyDefeated = true;
        return events;
      }

      startRecover(enemy);
    }
  }

  if (enemy.defeated) {
    return events;
  }

  enemy.phaseTimer = Math.max(0, enemy.phaseTimer - deltaSeconds);

  switch (enemy.phase) {
    case "chase": {
      const toPlayer = subtract(player.position, enemy.position);
      const targetDirection = normalize(toPlayer);
      const chaseDistance = distance(player.position, enemy.position);
      enemy.velocity = scale(targetDirection, enemy.speed);
      enemy.position = moveInsideBounds(
        add(enemy.position, scale(enemy.velocity, deltaSeconds)),
        enemy.radius,
        WORLD_BOUNDS
      );

      if (enemy.phaseTimer <= 0 || chaseDistance < 170) {
        startTelegraph(enemy, targetDirection);
      }
      break;
    }

    case "telegraph": {
      if (enemy.phaseTimer <= 0) {
        startStrike(enemy);
      }
      break;
    }

    case "strike": {
      enemy.velocity = scale(enemy.strikeDirection, 420);
      enemy.position = moveInsideBounds(
        add(enemy.position, scale(enemy.velocity, deltaSeconds)),
        enemy.radius,
        WORLD_BOUNDS
      );

      if (
        !enemy.hitPlayerThisStrike &&
        distance(player.position, enemy.position) <= player.radius + enemy.radius + 6
      ) {
        enemy.hitPlayerThisStrike = true;

        if (player.invulnerabilityTimer <= 0) {
          damagePlayer(player);
          player.position = moveInsideBounds(
            add(player.position, scale(enemy.strikeDirection, 26)),
            player.radius,
            WORLD_BOUNDS
          );
          events.playerDamaged = true;
        }
      }

      if (enemy.phaseTimer <= 0) {
        startRecover(enemy);
      }
      break;
    }

    case "recover": {
      if (enemy.phaseTimer <= 0) {
        enemy.phase = "chase";
        enemy.phaseTimer = 1.2;
      }
      break;
    }

    case "down": {
      break;
    }
  }

  return events;
}
