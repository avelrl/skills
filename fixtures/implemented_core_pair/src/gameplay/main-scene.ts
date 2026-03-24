import { createEnemy } from "./combat-loop";
import { WORLD_BOUNDS } from "./config";
import { createPlayer } from "./player-movement";
import { TAU } from "./shared";

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
  context.fillStyle = color;
  context.textAlign = align;
  context.fillText(value, x, y);
}

export class AssemblyPreviewScene {
  private elapsedSeconds = 0;
  private readonly player = createPlayer();
  private readonly enemy = createEnemy();

  update(deltaSeconds: number): void {
    this.elapsedSeconds += Math.min(deltaSeconds, 1 / 20);
  }

  render(context: CanvasRenderingContext2D): void {
    context.clearRect(0, 0, WORLD_BOUNDS.width, WORLD_BOUNDS.height);
    this.drawArena(context);
    this.drawImplementedMarkers(context);
    this.drawAssemblyCard(context);
  }

  private drawArena(context: CanvasRenderingContext2D): void {
    const gradient = context.createLinearGradient(0, 0, 0, WORLD_BOUNDS.height);
    gradient.addColorStop(0, "#0d1f2d");
    gradient.addColorStop(1, "#07111b");
    context.fillStyle = gradient;
    context.fillRect(0, 0, WORLD_BOUNDS.width, WORLD_BOUNDS.height);

    context.strokeStyle = "rgba(241, 181, 106, 0.18)";
    context.lineWidth = 2;
    context.strokeRect(16, 16, WORLD_BOUNDS.width - 32, WORLD_BOUNDS.height - 32);

    for (let index = 0; index < 12; index += 1) {
      const offset =
        (index * 96 + this.elapsedSeconds * 26) % (WORLD_BOUNDS.width + 120);
      context.fillStyle = "rgba(255, 255, 255, 0.025)";
      context.fillRect(offset - 100, 28, 56, WORLD_BOUNDS.height - 56);
    }
  }

  private drawImplementedMarkers(context: CanvasRenderingContext2D): void {
    const pulse = 1 + Math.sin(this.elapsedSeconds * 3.2) * 0.06;

    context.save();
    context.translate(this.player.position.x, this.player.position.y);
    context.fillStyle = "#4debdc";
    context.beginPath();
    context.arc(0, 0, this.player.radius * pulse, 0, TAU);
    context.fill();
    context.restore();

    context.save();
    context.translate(this.enemy.position.x, this.enemy.position.y);
    context.fillStyle = "#f15b5b";
    context.beginPath();
    context.arc(0, 0, this.enemy.radius * pulse, 0, TAU);
    context.fill();
    context.restore();

    drawText(
      context,
      "Implemented systems are present, but not yet assembled into one playable loop.",
      44,
      92,
      18,
      "rgba(230, 237, 231, 0.9)"
    );
  }

  private drawAssemblyCard(context: CanvasRenderingContext2D): void {
    const cardX = 560;
    const cardY = 136;
    const cardWidth = 340;
    const cardHeight = 258;

    context.fillStyle = "rgba(16, 21, 24, 0.82)";
    context.strokeStyle = "rgba(255, 211, 108, 0.35)";
    context.lineWidth = 2;
    context.beginPath();
    context.roundRect(cardX, cardY, cardWidth, cardHeight, 20);
    context.fill();
    context.stroke();

    drawText(context, "Assembly Preview", cardX + 24, cardY + 36, 24, "#ffd166");
    drawText(
      context,
      "Implemented modules:",
      cardX + 24,
      cardY + 72,
      16,
      "rgba(230, 237, 231, 0.88)"
    );
    drawText(
      context,
      "1. Player Movement",
      cardX + 40,
      cardY + 104,
      16,
      "rgba(77, 235, 220, 0.95)"
    );
    drawText(
      context,
      "2. Combat Loop",
      cardX + 40,
      cardY + 132,
      16,
      "rgba(241, 91, 91, 0.95)"
    );
    drawText(
      context,
      "Missing glue before first playable:",
      cardX + 24,
      cardY + 176,
      16,
      "rgba(230, 237, 231, 0.88)"
    );
    drawText(
      context,
      "- title/start flow\n- objective timer and gate\n- HUD and end states\n- assembly report",
      cardX + 40,
      cardY + 206,
      15,
      "rgba(192, 206, 214, 0.9)"
    );
  }
}
