import "./styles.css";

import { WORLD_BOUNDS } from "./gameplay/config";
import { AssemblyPreviewScene } from "./gameplay/main-scene";

const app = document.querySelector<HTMLDivElement>("#app");

if (!app) {
  throw new Error("Application root #app is missing");
}

app.innerHTML = `
  <main class="shell">
    <header class="shell__header">
      <p class="shell__eyebrow">Assembly prep snapshot</p>
      <h1 class="shell__title">Courier Drift</h1>
      <p class="shell__deck">
        Player Movement and Combat Loop are already implemented. The next task is to assemble them into one coherent playable slice.
      </p>
    </header>
    <section class="game-frame" aria-label="Courier Drift assembly preview">
      <canvas width="${WORLD_BOUNDS.width}" height="${WORLD_BOUNDS.height}"></canvas>
    </section>
    <footer class="shell__footer">
      <span>Implemented: Player Movement</span>
      <span>Implemented: Combat Loop</span>
      <span>Next: assemble first playable</span>
    </footer>
  </main>
`;

const canvas = app.querySelector<HTMLCanvasElement>("canvas");

if (!canvas) {
  throw new Error("Main game canvas is missing");
}

const context = canvas.getContext("2d");

if (!context) {
  throw new Error("2D canvas context is required");
}

const scene = new AssemblyPreviewScene();

let previousTime = performance.now();

function frame(currentTime: number): void {
  const deltaSeconds = (currentTime - previousTime) / 1000;
  previousTime = currentTime;
  scene.update(deltaSeconds);
  scene.render(context);
  window.requestAnimationFrame(frame);
}

scene.render(context);
window.requestAnimationFrame(frame);
