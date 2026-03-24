export interface GameManifest {
  id: string;
  title: string;
  tagline: string;
  targetSystem: string;
  buildGoal: string;
  districts: string[];
  todo: string[];
  palette: Record<string, string>;
}

export interface SceneUpdate {
  deltaSeconds: number;
  elapsedSeconds: number;
  input: ReadonlySet<string>;
  justPressed: ReadonlySet<string>;
}

export interface SceneRender {
  ctx: CanvasRenderingContext2D;
  manifest: GameManifest;
  width: number;
  height: number;
  elapsedSeconds: number;
  input: ReadonlySet<string>;
}

export interface Scene {
  update(frame: SceneUpdate): void;
  render(frame: SceneRender): void;
}

export class Game {
  private readonly ctx: CanvasRenderingContext2D;
  private readonly input = new Set<string>();
  private readonly justPressed = new Set<string>();
  private animationFrame = 0;
  private previousTime = 0;
  private elapsedSeconds = 0;

  constructor(
    private readonly canvas: HTMLCanvasElement,
    private readonly scene: Scene,
    private readonly manifest: GameManifest = {
      id: "scaffold",
      title: "Scaffold",
      tagline: "",
      targetSystem: "Unknown",
      buildGoal: "Scaffold only",
      districts: [],
      todo: [],
      palette: {}
    }
  ) {
    const context = this.canvas.getContext("2d");

    if (!context) {
      throw new Error("2D canvas context is unavailable.");
    }

    this.ctx = context;
  }

  start(): void {
    this.bindEvents();
    this.resize();
    this.animationFrame = requestAnimationFrame(this.loop);
  }

  stop(): void {
    cancelAnimationFrame(this.animationFrame);
    this.unbindEvents();
  }

  private readonly loop = (now: number): void => {
    const deltaSeconds = this.previousTime === 0 ? 0 : (now - this.previousTime) / 1000;

    this.previousTime = now;
    this.elapsedSeconds += deltaSeconds;

    this.scene.update({
      deltaSeconds,
      elapsedSeconds: this.elapsedSeconds,
      input: this.input,
      justPressed: this.justPressed
    });

    this.scene.render({
      ctx: this.ctx,
      manifest: this.manifest,
      width: this.canvas.width,
      height: this.canvas.height,
      elapsedSeconds: this.elapsedSeconds,
      input: this.input
    });

    this.justPressed.clear();
    this.animationFrame = requestAnimationFrame(this.loop);
  };

  private bindEvents(): void {
    window.addEventListener("resize", this.resize);
    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("keyup", this.handleKeyUp);
  }

  private unbindEvents(): void {
    window.removeEventListener("resize", this.resize);
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("keyup", this.handleKeyUp);
  }

  private readonly resize = (): void => {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    const nextWidth = Math.max(320, Math.floor(rect.width * dpr));
    const nextHeight = Math.max(180, Math.floor(rect.height * dpr));

    if (this.canvas.width !== nextWidth || this.canvas.height !== nextHeight) {
      this.canvas.width = nextWidth;
      this.canvas.height = nextHeight;
    }
  };

  private readonly handleKeyDown = (event: KeyboardEvent): void => {
    if (!this.input.has(event.code)) {
      this.justPressed.add(event.code);
    }

    this.input.add(event.code);
  };

  private readonly handleKeyUp = (event: KeyboardEvent): void => {
    this.input.delete(event.code);
  };
}
