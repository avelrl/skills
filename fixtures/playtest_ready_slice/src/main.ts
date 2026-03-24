import "./styles.css";

import { WORLD_BOUNDS } from "./gameplay/config";
import { FirstPlayableScene } from "./gameplay/main-scene";

const app = document.querySelector<HTMLDivElement>("#app");

if (!app) {
  throw new Error("Application root #app is missing");
}

app.innerHTML = `
  <main class="shell">
    <header class="shell__header">
      <p class="shell__eyebrow">First playable MVP</p>
      <h1 class="shell__title">Courier Drift</h1>
      <p class="shell__deck">
        Existing Player Movement and Combat Loop are now stitched into one runnable slice: defeat the interceptor, reach the relay gate, and restart the run if you fail.
      </p>
    </header>
    <section class="game-frame" aria-label="Courier Drift first playable MVP">
      <canvas width="${WORLD_BOUNDS.width}" height="${WORLD_BOUNDS.height}"></canvas>
    </section>
    <footer class="shell__footer">
      <span>Movement: WASD / Arrows</span>
      <span>Attack: Space</span>
      <span>Start: Enter</span>
      <span>Restart: R</span>
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

const scene = new FirstPlayableScene();

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
