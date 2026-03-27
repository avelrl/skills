import { createEnemy, updateCombatLoop } from "./combat-loop";
import {
  DELIVERY_DEADLINE,
  RELAY_GATE,
  RELAY_GATE_RADIUS,
  WORLD_BOUNDS
} from "./config";
import { createPlayer, updatePlayerMovement } from "./player-movement";
import { distance, TAU } from "./shared";
import type { EnemyState, InputState, PlayerState } from "./types";

type RunState = "boot" | "playing" | "won" | "lost";
type LossReason = "health" | "deadline" | null;

const FRAME_LIMIT = 1 / 20;

class InputController {
  private readonly heldKeys = new Set<string>();
  private attackQueued = false;
  private startQueued = false;
  private restartQueued = false;

  constructor() {
    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("keyup", this.handleKeyUp);
    window.addEventListener("blur", this.handleBlur);
  }

  snapshot(): InputState {
    const input: InputState = {
      up: this.isHeld("ArrowUp", "KeyW"),
      down: this.isHeld("ArrowDown", "KeyS"),
      left: this.isHeld("ArrowLeft", "KeyA"),
      right: this.isHeld("ArrowRight", "KeyD"),
      attackPressed: this.attackQueued,
      startPressed: this.startQueued,
      restartPressed: this.restartQueued
    };

    this.attackQueued = false;
    this.startQueued = false;
    this.restartQueued = false;

    return input;
  }

  private readonly handleKeyDown = (event: KeyboardEvent): void => {
    if (this.isManagedCode(event.code)) {
      event.preventDefault();
    }

    this.heldKeys.add(event.code);

    if (event.repeat) {
      return;
    }

    if (event.code === "Space") {
      this.attackQueued = true;
    }

    if (event.code === "Enter") {
      this.startQueued = true;
    }

    if (event.code === "KeyR") {
      this.restartQueued = true;
    }
  };

  private readonly handleKeyUp = (event: KeyboardEvent): void => {
    this.heldKeys.delete(event.code);
  };

  private readonly handleBlur = (): void => {
    this.heldKeys.clear();
  };

  private isHeld(...codes: string[]): boolean {
    return codes.some((code) => this.heldKeys.has(code));
  }

  private isManagedCode(code: string): boolean {
    return (
      code.startsWith("Arrow") ||
      code === "KeyW" ||
      code === "KeyA" ||
      code === "KeyS" ||
      code === "KeyD" ||
      code === "Space" ||
      code === "Enter" ||
      code === "KeyR"
    );
  }
}

function drawText(
  context: CanvasRenderingContext2D,
  value: string,
  x: number,
  y: number,
  size: number,
  color: string,
  align: CanvasTextAlign = "left"
): void {
  context.font = `${size}px "Avenir Next", "Trebuchet MS", sans-serif`;
  context.textAlign = align;
  context.textBaseline = "top";
  context.fillStyle = color;
  context.fillText(value, x, y);
}

function drawPanel(
  context: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number
): void {
  context.fillStyle = "rgba(6, 14, 23, 0.8)";
  context.strokeStyle = "rgba(255, 255, 255, 0.08)";
  context.lineWidth = 1.5;
  context.beginPath();
  context.roundRect(x, y, width, height, 18);
  context.fill();
  context.stroke();
}

function drawLines(
  context: CanvasRenderingContext2D,
  lines: string[],
  x: number,
  y: number,
  size: number,
  color: string,
  lineHeight: number,
  align: CanvasTextAlign = "left"
): void {
  lines.forEach((line, index) => {
    drawText(context, line, x, y + index * lineHeight, size, color, align);
  });
}

export class FirstPlayableScene {
  private readonly input = new InputController();
  private elapsedSeconds = 0;
  private state: RunState = "boot";
  private lossReason: LossReason = null;
  private player: PlayerState = createPlayer();
  private enemy: EnemyState = createEnemy();
  private deadlineRemaining = DELIVERY_DEADLINE;
  private gateUnlocked = false;
  private playerFlashTimer = 0;
  private enemyFlashTimer = 0;

  update(deltaSeconds: number): void {
    const step = Math.min(deltaSeconds, FRAME_LIMIT);
    const input = this.input.snapshot();

    this.elapsedSeconds += step;
    this.playerFlashTimer = Math.max(0, this.playerFlashTimer - step);
    this.enemyFlashTimer = Math.max(0, this.enemyFlashTimer - step);

    if (this.state === "boot") {
      if (input.startPressed) {
        this.startRun();
      }

      return;
    }

    if (this.state === "playing") {
      this.deadlineRemaining = Math.max(0, this.deadlineRemaining - step);

      updatePlayerMovement(this.player, input, step);

      const combatEvents = updateCombatLoop(this.player, this.enemy, step);
      this.gateUnlocked = this.enemy.defeated;

      if (combatEvents.playerDamaged) {
        this.playerFlashTimer = 0.3;
      }

      if (combatEvents.enemyDamaged) {
        this.enemyFlashTimer = 0.18;
      }

      if (this.player.health <= 0) {
        this.state = "lost";
        this.lossReason = "health";
        return;
      }

      if (
        this.gateUnlocked &&
        distance(this.player.position, RELAY_GATE) <= RELAY_GATE_RADIUS
      ) {
        this.state = "won";
        this.lossReason = null;
        return;
      }

      if (this.deadlineRemaining <= 0) {
        this.state = "lost";
        this.lossReason = "deadline";
      }

      return;
    }

    if (input.restartPressed || input.startPressed) {
      this.startRun();
    }
  }

  render(context: CanvasRenderingContext2D): void {
    context.clearRect(0, 0, WORLD_BOUNDS.width, WORLD_BOUNDS.height);
    this.drawArena(context);
    this.drawRelayGate(context);
    this.drawEnemy(context);
    this.drawPlayer(context);
    this.drawHud(context);

    if (this.state === "boot") {
      this.drawBootOverlay(context);
    } else if (this.state === "won") {
      this.drawEndOverlay(
        context,
        "Delivery Complete",
        "Combat loop cleared. Relay synchronized before the deadline.",
        "#4debdc"
      );
    } else if (this.state === "lost") {
      const message =
        this.lossReason === "health"
          ? "The interceptor broke the run before the package reached the gate."
          : "The relay window closed before the delivery could be completed.";

      this.drawEndOverlay(context, "Run Failed", message, "#f15b5b");
    }
  }

  private startRun(): void {
    this.player = createPlayer();
    this.enemy = createEnemy();
    this.deadlineRemaining = DELIVERY_DEADLINE;
    this.gateUnlocked = false;
    this.playerFlashTimer = 0;
    this.enemyFlashTimer = 0;
    this.lossReason = null;
    this.state = "playing";
  }

  private drawArena(context: CanvasRenderingContext2D): void {
    const gradient = context.createLinearGradient(0, 0, 0, WORLD_BOUNDS.height);
    gradient.addColorStop(0, "#102536");
    gradient.addColorStop(1, "#07111b");
    context.fillStyle = gradient;
    context.fillRect(0, 0, WORLD_BOUNDS.width, WORLD_BOUNDS.height);

    for (let index = 0; index < 12; index += 1) {
      const offset =
        (index * 96 + this.elapsedSeconds * 34) % (WORLD_BOUNDS.width + 150);

      context.fillStyle = "rgba(255, 255, 255, 0.022)";
      context.fillRect(offset - 120, 22, 72, WORLD_BOUNDS.height - 44);
    }

    context.strokeStyle = "rgba(241, 181, 106, 0.18)";
    context.lineWidth = 2;
    context.strokeRect(16, 16, WORLD_BOUNDS.width - 32, WORLD_BOUNDS.height - 32);

    context.strokeStyle = "rgba(255, 255, 255, 0.04)";
    context.setLineDash([10, 12]);
    context.beginPath();
    context.moveTo(280, 24);
    context.lineTo(280, WORLD_BOUNDS.height - 24);
    context.moveTo(680, 24);
    context.lineTo(680, WORLD_BOUNDS.height - 24);
    context.stroke();
    context.setLineDash([]);
  }

  private drawRelayGate(context: CanvasRenderingContext2D): void {
    const pulse = 1 + Math.sin(this.elapsedSeconds * 3.6) * 0.08;
    const radius = RELAY_GATE_RADIUS * pulse;
    const isOpen = this.gateUnlocked;

    context.save();
    context.translate(RELAY_GATE.x, RELAY_GATE.y);

    context.fillStyle = isOpen
      ? "rgba(77, 235, 220, 0.16)"
      : "rgba(241, 91, 91, 0.08)";
    context.beginPath();
    context.arc(0, 0, radius + 10, 0, TAU);
    context.fill();

    context.strokeStyle = isOpen ? "#4debdc" : "rgba(241, 91, 91, 0.55)";
    context.lineWidth = 4;
    context.beginPath();
    context.arc(0, 0, radius, 0, TAU);
    context.stroke();

    context.strokeStyle = "rgba(255, 255, 255, 0.28)";
    context.lineWidth = 1.5;
    context.setLineDash([6, 8]);
    context.beginPath();
    context.arc(0, 0, radius - 10, 0, TAU);
    context.stroke();
    context.setLineDash([]);

    drawText(
      context,
      isOpen ? "RELAY OPEN" : "RELAY LOCKED",
      0,
      radius + 18,
      14,
      isOpen ? "#91fff3" : "rgba(255, 217, 217, 0.92)",
      "center"
    );
    context.restore();
  }

  private drawEnemy(context: CanvasRenderingContext2D): void {
    if (!this.enemy.defeated && this.enemy.phase === "telegraph") {
      context.save();
      context.translate(this.enemy.position.x, this.enemy.position.y);
      context.strokeStyle = "rgba(255, 209, 102, 0.9)";
      context.lineWidth = 5;
      context.beginPath();
      context.moveTo(0, 0);
      context.lineTo(
        this.enemy.strikeDirection.x * 132,
        this.enemy.strikeDirection.y * 132
      );
      context.stroke();

      context.fillStyle = "rgba(255, 209, 102, 0.16)";
      context.beginPath();
      context.arc(0, 0, 44, 0, TAU);
      context.fill();
      context.restore();
    }

    if (!this.enemy.defeated && this.enemy.phase === "strike") {
      context.save();
      context.translate(this.enemy.position.x, this.enemy.position.y);
      context.strokeStyle = "rgba(241, 91, 91, 0.35)";
      context.lineWidth = 12;
      context.beginPath();
      context.moveTo(
        -this.enemy.strikeDirection.x * 34,
        -this.enemy.strikeDirection.y * 34
      );
      context.lineTo(
        this.enemy.strikeDirection.x * 54,
        this.enemy.strikeDirection.y * 54
      );
      context.stroke();
      context.restore();
    }

    context.save();
    context.translate(this.enemy.position.x, this.enemy.position.y);

    if (this.enemy.defeated) {
      context.fillStyle = "rgba(241, 91, 91, 0.18)";
      context.strokeStyle = "rgba(255, 255, 255, 0.18)";
    } else if (this.enemyFlashTimer > 0) {
      context.fillStyle = "#ffd166";
      context.strokeStyle = "#fff3d0";
    } else {
      context.fillStyle = "#f15b5b";
      context.strokeStyle = "rgba(255, 255, 255, 0.24)";
    }

    context.lineWidth = 2;
    context.beginPath();
    context.arc(0, 0, this.enemy.radius, 0, TAU);
    context.fill();
    context.stroke();

    if (this.enemy.defeated) {
      context.strokeStyle = "rgba(255, 255, 255, 0.3)";
      context.lineWidth = 3;
      context.beginPath();
      context.moveTo(-8, -8);
      context.lineTo(8, 8);
      context.moveTo(8, -8);
      context.lineTo(-8, 8);
      context.stroke();
    }

    context.restore();
  }

  private drawPlayer(context: CanvasRenderingContext2D): void {
    const facingAngle = Math.atan2(this.player.facing.y, this.player.facing.x);
    const blink =
      this.player.invulnerabilityTimer > 0 &&
      Math.floor(this.elapsedSeconds * 14) % 2 === 0;

    if (this.player.attackTimer > 0) {
      context.save();
      context.translate(this.player.position.x, this.player.position.y);
      context.strokeStyle = "rgba(255, 209, 102, 0.9)";
      context.lineWidth = 6;
      context.beginPath();
      context.arc(0, 0, this.player.radius + 26, facingAngle - 0.55, facingAngle + 0.55);
      context.stroke();
      context.restore();
    }

    context.save();
    context.translate(this.player.position.x, this.player.position.y);
    context.globalAlpha = blink ? 0.45 : 1;

    context.fillStyle = this.playerFlashTimer > 0 ? "#ffd166" : "#4debdc";
    context.strokeStyle = "rgba(255, 255, 255, 0.3)";
    context.lineWidth = 2;
    context.beginPath();
    context.arc(0, 0, this.player.radius, 0, TAU);
    context.fill();
    context.stroke();

    context.strokeStyle = "#d7fff8";
    context.lineWidth = 3;
    context.beginPath();
    context.moveTo(0, 0);
    context.lineTo(this.player.facing.x * 18, this.player.facing.y * 18);
    context.stroke();
    context.restore();
  }

  private drawHud(context: CanvasRenderingContext2D): void {
    drawPanel(context, 24, 24, 320, 112);
    drawText(context, "FIRST PLAYABLE", 44, 42, 14, "#f1b56a");
    drawText(context, this.getObjectiveLabel(), 44, 66, 24, "#edf3f8");
    drawLines(
      context,
      this.gateUnlocked
        ? ["Enemy down.", "Move into the relay ring to complete the run."]
        : ["Bait telegraphs with movement.", "Strike with Space during safe windows."],
      44,
      98,
      14,
      "rgba(237, 243, 248, 0.72)",
      18
    );

    drawPanel(context, 688, 24, 248, 124);
    drawText(context, "DEADLINE", 708, 42, 14, "#f1b56a");
    drawText(
      context,
      `${this.deadlineRemaining.toFixed(1)}s`,
      708,
      66,
      30,
      this.deadlineRemaining <= 10 ? "#ff8b8b" : "#edf3f8"
    );
    drawText(context, "HEALTH", 708, 104, 14, "#f1b56a");
    drawText(
      context,
      `${this.player.health}/${this.player.maxHealth}`,
      708,
      126,
      20,
      this.player.health <= 1 ? "#ff8b8b" : "#91fff3"
    );

    drawPanel(context, 24, 436, 472, 80);
    drawText(
      context,
      "Move: WASD / Arrows",
      44,
      454,
      15,
      "rgba(237, 243, 248, 0.88)"
    );
    drawText(
      context,
      "Attack: Space",
      238,
      454,
      15,
      "rgba(237, 243, 248, 0.88)"
    );
    drawText(
      context,
      "Start: Enter",
      366,
      454,
      15,
      "rgba(237, 243, 248, 0.88)"
    );
    drawText(
      context,
      "Restart: R",
      44,
      482,
      15,
      "rgba(237, 243, 248, 0.72)"
    );
    drawText(
      context,
      "Enemy HP",
      708,
      454,
      14,
      "rgba(237, 243, 248, 0.72)"
    );
    drawText(
      context,
      `${Math.max(0, this.enemy.health)}/${this.enemy.maxHealth}`,
      708,
      476,
      22,
      this.enemy.defeated ? "#4debdc" : "#ffd166"
    );
    drawText(
      context,
      this.enemy.defeated ? "Down" : this.enemy.phase.toUpperCase(),
      822,
      476,
      18,
      this.enemy.defeated ? "#4debdc" : "rgba(237, 243, 248, 0.88)"
    );
  }

  private drawBootOverlay(context: CanvasRenderingContext2D): void {
    drawPanel(context, 208, 136, 544, 244);
    drawText(context, "Courier Drift", 480, 164, 34, "#edf3f8", "center");
    drawText(context, "First playable MVP", 480, 204, 18, "#f1b56a", "center");
    drawLines(
      context,
      [
        "Defeat the interceptor, then deliver the package",
        "through the relay gate before the window closes."
      ],
      480,
      244,
      16,
      "rgba(237, 243, 248, 0.8)",
      22,
      "center"
    );
    drawLines(
      context,
      [
        "Movement and combat are wired into one run",
        "with a fail state and restart flow."
      ],
      480,
      290,
      16,
      "rgba(237, 243, 248, 0.8)",
      22,
      "center"
    );
    drawText(context, "Press Enter to start", 480, 344, 20, "#91fff3", "center");
  }

  private drawEndOverlay(
    context: CanvasRenderingContext2D,
    title: string,
    message: string,
    accent: string
  ): void {
    drawPanel(context, 220, 164, 520, 212);
    drawText(context, title, 480, 194, 32, accent, "center");
    drawLines(
      context,
      title === "Run Failed"
        ? [
            "The run ended before the package could be delivered.",
            message
          ]
        : ["Combat loop cleared.", message],
      480,
      248,
      17,
      "rgba(237, 243, 248, 0.82)",
      24,
      "center"
    );
    drawText(
      context,
      "Press Enter or R to run again",
      480,
      318,
      18,
      "#edf3f8",
      "center"
    );
  }

  private getObjectiveLabel(): string {
    if (this.state === "won") {
      return "Run complete";
    }

    if (this.state === "lost") {
      return "Run failed";
    }

    if (this.gateUnlocked) {
      return "Reach the relay gate";
    }

    return "Defeat the interceptor";
  }
}
