import manifest from "../data/game-manifest.json";
import { Game } from "./game/Game";
import { BootScene } from "./game/scenes/BootScene";
import "./styles.css";

const canvas = document.querySelector<HTMLCanvasElement>("#game");

if (!canvas) {
  throw new Error("Expected #game canvas to exist.");
}

const buildStatus = document.querySelector<HTMLElement>("[data-build-status]");

if (buildStatus) {
  buildStatus.textContent =
    `${manifest.title} scaffold is bootable. Target system: ${manifest.targetSystem}.`;
}

const scene = new BootScene(manifest);
const game = new Game(canvas, scene, manifest);

game.start();
