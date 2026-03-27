import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import process from "node:process";
import { fileURLToPath } from "node:url";

const MODULE_PATH = fileURLToPath(import.meta.url);
const MODULE_DIR = path.dirname(MODULE_PATH);
const SKILL_DIR = path.resolve(MODULE_DIR, "..");

export function resolveCodexHome() {
  if (process.env.CODEX_HOME) {
    return path.resolve(process.env.CODEX_HOME);
  }
  if (process.env.HOME) {
    return path.join(process.env.HOME, ".codex");
  }
  throw new Error("Cannot resolve CODEX_HOME because both CODEX_HOME and HOME are unset.");
}

function runtimeDirForCodexHome() {
  return path.join(resolveCodexHome(), "runtimes", "web-ui-smoke");
}

function runtimeDirFromLocalSkill() {
  return SKILL_DIR;
}

export function buildRuntimeCandidates({ runtimeDir } = {}) {
  const seen = new Set();
  const candidates = [];

  const pushCandidate = (dirPath, source) => {
    if (!dirPath) return;
    const resolved = path.resolve(dirPath);
    if (seen.has(resolved)) return;
    seen.add(resolved);
    candidates.push({
      dir: resolved,
      source,
      packageJsonPath: path.join(resolved, "node_modules", "playwright", "package.json"),
      browsersPath: path.join(resolved, "browsers"),
    });
  };

  if (runtimeDir) {
    pushCandidate(runtimeDir, "CLI runtime");
  }
  if (process.env.WEB_UI_SMOKE_RUNTIME_DIR) {
    pushCandidate(process.env.WEB_UI_SMOKE_RUNTIME_DIR, "WEB_UI_SMOKE_RUNTIME_DIR");
  }

  pushCandidate(runtimeDirForCodexHome(), "CODEX_HOME runtime");
  pushCandidate(runtimeDirFromLocalSkill(), "local skill fallback");
  return candidates;
}

export function formatRuntimeCandidates(candidates) {
  return candidates
    .map((candidate) => `- ${candidate.source}: ${candidate.dir}`)
    .join("\n");
}

export function resolvePlaywrightRuntime({ runtimeDir } = {}) {
  const candidates = buildRuntimeCandidates({ runtimeDir });
  const loadErrors = [];

  for (const candidate of candidates) {
    if (!fs.existsSync(candidate.packageJsonPath)) {
      continue;
    }

    try {
      if (!process.env.PLAYWRIGHT_BROWSERS_PATH && candidate.source !== "local skill fallback") {
        process.env.PLAYWRIGHT_BROWSERS_PATH = candidate.browsersPath;
      }

      const runtimeRequire = createRequire(path.join(candidate.dir, "__web_ui_smoke_runtime__.cjs"));
      const packagePath = runtimeRequire.resolve("playwright/package.json");
      const playwright = runtimeRequire("playwright");

      return {
        playwright,
        runtimeInfo: {
          runtimeDir: candidate.dir,
          browsersPath: process.env.PLAYWRIGHT_BROWSERS_PATH || "(default Playwright cache)",
          packagePath,
          source: candidate.source,
        },
        candidates,
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      loadErrors.push(`${candidate.source}: ${message}`);
    }
  }

  const installCommand =
    'Resolve the installed absolute path to install_runtime.sh and run it directly, for example /absolute/path/to/.codex/skills/web-ui-smoke/scripts/install_runtime.sh';
  const details = loadErrors.length > 0 ? `\nLoad errors:\n${loadErrors.map((entry) => `- ${entry}`).join("\n")}` : "";

  throw new Error(
    `Cannot import "playwright" for web-ui-smoke.\n` +
    `Checked runtime directories:\n${formatRuntimeCandidates(candidates)}\n` +
    `Install the shared runtime with:\n${installCommand}\n` +
    `Do not add repo-local shims such as node_modules/playwright.${details}`
  );
}
