import type { GameManifest, Scene, SceneRender, SceneUpdate } from "../Game";

const movementKeys = [
  "ArrowUp",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "KeyW",
  "KeyA",
  "KeyS",
  "KeyD"
];

export class BootScene implements Scene {
  private showTodo = false;
  private routePulse = 0;
  private activeKeysLabel = "none";

  constructor(private readonly manifest: GameManifest) {}

  update({ deltaSeconds, justPressed, input }: SceneUpdate): void {
    if (justPressed.has("Enter")) {
      this.showTodo = !this.showTodo;
    }

    if (justPressed.has("KeyR")) {
      this.routePulse = 1;
    }

    this.routePulse = Math.max(0, this.routePulse - deltaSeconds * 1.4);
    this.activeKeysLabel = this.collectMovementKeys(input);
  }

  render({ ctx, width, height, elapsedSeconds }: SceneRender): void {
    const palette = this.manifest.palette;
    const pulse = Math.max(0.15, this.routePulse);

    ctx.clearRect(0, 0, width, height);

    const sky = ctx.createLinearGradient(0, 0, 0, height);
    sky.addColorStop(0, palette.sky);
    sky.addColorStop(0.35, palette.smog);
    sky.addColorStop(1, palette.asphalt);
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, width, height);

    this.drawBackdrop(ctx, width, height, elapsedSeconds, pulse);
    this.drawCourierMarker(ctx, width, height, elapsedSeconds);
    this.drawRoute(ctx, width, height, pulse);
    this.drawHud(ctx, width, height);
  }

  private drawBackdrop(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    elapsedSeconds: number,
    pulse: number
  ): void {
    ctx.save();
    ctx.globalAlpha = 0.18 + pulse * 0.2;
    ctx.strokeStyle = this.manifest.palette.signal;
    ctx.lineWidth = 1;

    for (let x = -40; x < width + 40; x += 48) {
      const drift = Math.sin(elapsedSeconds * 0.45 + x * 0.02) * 8;
      ctx.beginPath();
      ctx.moveTo(x + drift, 0);
      ctx.lineTo(x - drift, height);
      ctx.stroke();
    }

    ctx.restore();

    ctx.save();
    ctx.fillStyle = "rgba(12, 16, 19, 0.32)";

    for (let i = 0; i < 6; i += 1) {
      const baseX = width * (0.1 + i * 0.14);
      const towerHeight = height * (0.18 + ((i + 1) % 3) * 0.11);
      ctx.fillRect(baseX, height - towerHeight - 30, 24, towerHeight);
      ctx.fillRect(baseX + 30, height - towerHeight * 0.7 - 30, 18, towerHeight * 0.7);
    }

    ctx.restore();
  }

  private drawCourierMarker(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    elapsedSeconds: number
  ): void {
    const centerX = width * 0.32;
    const centerY = height * 0.58;
    const bob = Math.sin(elapsedSeconds * 2.2) * 4;

    ctx.save();
    ctx.translate(centerX, centerY + bob);

    ctx.fillStyle = this.manifest.palette.signal;
    ctx.beginPath();
    ctx.arc(0, 0, 18, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = this.manifest.palette.accent;
    ctx.beginPath();
    ctx.moveTo(-10, 24);
    ctx.lineTo(14, 0);
    ctx.lineTo(-10, -24);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = this.manifest.palette.warning;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, 36 + Math.sin(elapsedSeconds * 3) * 4, 0, Math.PI * 2);
    ctx.stroke();

    ctx.restore();
  }

  private drawRoute(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    pulse: number
  ): void {
    ctx.save();
    ctx.strokeStyle = this.manifest.palette.accent;
    ctx.lineWidth = 6;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.globalAlpha = 0.35 + pulse * 0.5;

    ctx.beginPath();
    ctx.moveTo(width * 0.33, height * 0.58);
    ctx.lineTo(width * 0.48, height * 0.5);
    ctx.lineTo(width * 0.58, height * 0.56);
    ctx.lineTo(width * 0.71, height * 0.41);
    ctx.lineTo(width * 0.85, height * 0.32);
    ctx.stroke();

    ctx.fillStyle = this.manifest.palette.warning;
    ctx.beginPath();
    ctx.arc(width * 0.85, height * 0.32, 12, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  private drawHud(ctx: CanvasRenderingContext2D, width: number, height: number): void {
    const cardWidth = Math.min(420, width * 0.42);
    const cardHeight = Math.min(260, height * 0.42);
    const x = width - cardWidth - 36;
    const y = 30;

    ctx.save();
    ctx.fillStyle = "rgba(16, 21, 24, 0.78)";
    ctx.strokeStyle = "rgba(255, 211, 108, 0.35)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(x, y, cardWidth, cardHeight, 20);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = this.manifest.palette.signal;
    ctx.font = "600 18px 'Avenir Next Condensed', 'Trebuchet MS', sans-serif";
    ctx.fillText(this.showTodo ? "Boot TODOs" : "Scaffold Brief", x + 24, y + 34);

    ctx.fillStyle = "rgba(230, 237, 231, 0.72)";
    ctx.font = "500 12px 'IBM Plex Mono', 'Courier New', monospace";
    ctx.fillText(`movement input: ${this.activeKeysLabel}`, x + 24, y + 58);

    ctx.fillStyle = this.manifest.palette.signal;
    ctx.font = "400 15px 'Avenir Next Condensed', 'Trebuchet MS', sans-serif";
    const rows = (this.showTodo ? this.manifest.todo : this.buildOverview()).flatMap((row) =>
      this.wrapRow(ctx, row, cardWidth - 48)
    );

    rows.forEach((row, index) => {
      const lineY = y + 92 + index * 28;
      ctx.fillText(row, x + 24, lineY);
    });

    ctx.fillStyle = "rgba(255, 139, 61, 0.95)";
    ctx.font = "600 13px 'IBM Plex Mono', 'Courier New', monospace";
    ctx.fillText("ENTER: panel  |  R: route pulse", x + 24, y + cardHeight - 24);

    ctx.restore();
  }

  private buildOverview(): string[] {
    return [
      this.manifest.tagline,
      `Target system: ${this.manifest.targetSystem}`,
      `Build goal: ${this.manifest.buildGoal}`,
      `District seeds: ${this.manifest.districts.join(", ")}`
    ];
  }

  private collectMovementKeys(input: ReadonlySet<string>): string {
    const active = movementKeys.filter((key) => input.has(key));
    return active.length === 0 ? "none" : active.join(" ");
  }

  private wrapRow(
    ctx: CanvasRenderingContext2D,
    text: string,
    maxWidth: number
  ): string[] {
    const words = text.split(" ");
    const lines: string[] = [];
    let currentLine = "";

    for (const word of words) {
      const nextLine = currentLine === "" ? word : `${currentLine} ${word}`;

      if (ctx.measureText(nextLine).width <= maxWidth) {
        currentLine = nextLine;
        continue;
      }

      if (currentLine !== "") {
        lines.push(currentLine);
      }

      currentLine = word;
    }

    if (currentLine !== "") {
      lines.push(currentLine);
    }

    return lines;
  }
}
