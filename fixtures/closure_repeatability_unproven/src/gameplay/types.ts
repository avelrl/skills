export interface Vector2 {
  x: number;
  y: number;
}

export interface Bounds {
  width: number;
  height: number;
}

export interface InputState {
  up: boolean;
  down: boolean;
  left: boolean;
  right: boolean;
  attackPressed: boolean;
  startPressed: boolean;
  restartPressed: boolean;
}

export interface PlayerState {
  position: Vector2;
  velocity: Vector2;
  facing: Vector2;
  radius: number;
  speed: number;
  health: number;
  maxHealth: number;
  attackCooldown: number;
  attackTimer: number;
  attackId: number;
  invulnerabilityTimer: number;
}

export type EnemyPhase = "chase" | "telegraph" | "strike" | "recover" | "down";

export interface EnemyState {
  position: Vector2;
  velocity: Vector2;
  radius: number;
  speed: number;
  health: number;
  maxHealth: number;
  phase: EnemyPhase;
  phaseTimer: number;
  strikeDirection: Vector2;
  hitPlayerThisStrike: boolean;
  lastRegisteredAttackId: number;
  defeated: boolean;
}

export interface CombatEvents {
  playerDamaged: boolean;
  enemyDamaged: boolean;
  enemyDefeated: boolean;
}
