import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { buildRuntimeCandidates, resolvePlaywrightRuntime } from "./playwright_runtime.mjs";

function parseBoolean(value, defaultValue) {
  if (value === undefined || value === null) return defaultValue;
  return !["0", "false", "no", "off"].includes(String(value).toLowerCase());
}

function parseInteger(value, defaultValue) {
  const parsed = Number.parseInt(String(value), 10);
  return Number.isFinite(parsed) ? parsed : defaultValue;
}

function parseArgs(argv) {
  const args = {
    url: null,
    actionsFile: null,
    actionsJson: null,
    screenshotDir: ".codex-artifacts/web-ui",
    runtimeDir: null,
    headless: true,
    timeoutMs: 10000,
    viewportWidth: 1440,
    viewportHeight: 1200,
    allowErrors: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === "--url" && next) {
      args.url = next;
      i++;
    } else if (arg === "--actions-file" && next) {
      args.actionsFile = next;
      i++;
    } else if (arg === "--actions-json" && next) {
      args.actionsJson = next;
      i++;
    } else if (arg === "--screenshot-dir" && next) {
      args.screenshotDir = next;
      i++;
    } else if (arg === "--runtime-dir" && next) {
      args.runtimeDir = next;
      i++;
    } else if (arg === "--headless" && next) {
      args.headless = parseBoolean(next, true);
      i++;
    } else if (arg === "--timeout-ms" && next) {
      args.timeoutMs = parseInteger(next, 10000);
      i++;
    } else if (arg === "--viewport-width" && next) {
      args.viewportWidth = parseInteger(next, 1440);
      i++;
    } else if (arg === "--viewport-height" && next) {
      args.viewportHeight = parseInteger(next, 1200);
      i++;
    } else if (arg === "--allow-errors" && next) {
      args.allowErrors = parseBoolean(next, false);
      i++;
    }
  }

  if (!args.url) {
    throw new Error("--url is required");
  }
  if (!args.actionsFile && !args.actionsJson) {
    throw new Error("Use --actions-file or --actions-json");
  }
  return args;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function clearManagedArtifacts(outDir) {
  if (!fs.existsSync(outDir)) {
    return;
  }

  for (const entry of fs.readdirSync(outDir, { withFileTypes: true })) {
    if (!entry.isFile()) {
      continue;
    }

    const managed =
      entry.name === "summary.json" ||
      entry.name === "bootstrap-error.json" ||
      entry.name.endsWith(".png");

    if (!managed) {
      continue;
    }

    fs.rmSync(path.join(outDir, entry.name), { force: true });
  }
}

function loadSteps(args) {
  const raw = args.actionsFile
    ? fs.readFileSync(args.actionsFile, "utf-8")
    : args.actionsJson;
  const parsed = JSON.parse(raw);
  if (Array.isArray(parsed)) return parsed;
  if (parsed && Array.isArray(parsed.steps)) return parsed.steps;
  throw new Error("Actions payload must be an array or an object with a steps array");
}

function normalizeUrl(candidate, baseUrl) {
  if (!candidate) return baseUrl;
  if (/^(https?:|file:|data:)/.test(candidate)) return candidate;
  return new URL(candidate, baseUrl).toString();
}

function sanitizeName(name) {
  return String(name || "shot")
    .replace(/[^a-zA-Z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "") || "shot";
}

function truncate(text, limit = 500) {
  const value = String(text ?? "");
  return value.length <= limit ? value : `${value.slice(0, limit)}…`;
}

function locatorFor(page, selector, timeoutMs) {
  if (!selector) {
    throw new Error("selector is required for this operation");
  }
  return page.locator(selector).first();
}

function writeBootstrapError(outDir, stage, error, diagnostics = {}) {
  const message = error instanceof Error ? error.message : String(error);
  const payload = {
    stage,
    message,
    diagnostics,
  };

  try {
    fs.writeFileSync(path.join(outDir, "bootstrap-error.json"), JSON.stringify(payload, null, 2));
  } catch {
    // ignore bootstrap artifact write failures; original error is more important
  }
}

async function launchChromium(playwright, runtimeInfo, args) {
  try {
    return await playwright.chromium.launch({
      headless: args.headless,
      args: ["--use-gl=angle", "--use-angle=swiftshader"],
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const guidance =
      message.includes("Executable doesn't exist")
        ? `Playwright loaded from ${runtimeInfo.runtimeDir}, but the Chromium executable is missing for this runtime. Install browsers into ${runtimeInfo.browsersPath} or switch to web-ui-doctor.`
        : "Chromium launch failed before the app flow started. Switch to web-ui-doctor to classify sandbox/runtime vs browser-install issues.";
    throw new Error(`${guidance}\nOriginal error: ${message}`);
  }
}

class EventTracker {
  constructor() {
    this.consoleErrors = [];
    this.pageErrors = [];
    this.requestFailures = [];
  }

  attach(page) {
    page.on("console", (msg) => {
      if (msg.type() !== "error") return;
      this.consoleErrors.push({
        type: "console.error",
        text: msg.text(),
        location: msg.location(),
      });
    });
    page.on("pageerror", (err) => {
      this.pageErrors.push({
        type: "pageerror",
        text: String(err),
      });
    });
    page.on("requestfailed", (request) => {
      this.requestFailures.push({
        type: "requestfailed",
        method: request.method(),
        url: request.url(),
        failure: request.failure(),
      });
    });
  }

  hasErrors() {
    return this.consoleErrors.length > 0 || this.pageErrors.length > 0 || this.requestFailures.length > 0;
  }

  toJSON() {
    return {
      consoleErrors: this.consoleErrors,
      pageErrors: this.pageErrors,
      requestFailures: this.requestFailures,
    };
  }
}

async function getText(locator) {
  const text = await locator.innerText();
  return String(text ?? "").trim();
}

async function executeStep(page, step, context) {
  const op = step.op;
  if (!op) {
    throw new Error("Each step must include op");
  }

  switch (op) {
    case "goto": {
      const target = normalizeUrl(step.url, context.baseUrl);
      await page.goto(target, { waitUntil: step.waitUntil || "domcontentloaded", timeout: step.timeoutMs || context.timeoutMs });
      context.currentUrl = target;
      return { ok: true, detail: `goto ${target}` };
    }
    case "click": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.click({ timeout: step.timeoutMs || context.timeoutMs, button: step.button || "left", clickCount: step.clickCount || 1 });
      return { ok: true, detail: `click ${step.selector}` };
    }
    case "fill": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.fill(String(step.text ?? ""), { timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `fill ${step.selector}` };
    }
    case "type": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.click({ timeout: step.timeoutMs || context.timeoutMs });
      await locator.type(String(step.text ?? ""), { delay: step.delayMs || 0, timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `type ${step.selector}` };
    }
    case "press": {
      if (step.selector) {
        const locator = locatorFor(page, step.selector, context.timeoutMs);
        await locator.press(String(step.key), { timeout: step.timeoutMs || context.timeoutMs });
      } else {
        await page.keyboard.press(String(step.key));
      }
      return { ok: true, detail: `press ${step.key}` };
    }
    case "hover": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.hover({ timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `hover ${step.selector}` };
    }
    case "select": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.selectOption(step.value, { timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `select ${step.selector}` };
    }
    case "check": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.check({ timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `check ${step.selector}` };
    }
    case "uncheck": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.uncheck({ timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `uncheck ${step.selector}` };
    }
    case "waitForSelector": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await locator.waitFor({ state: step.state || "visible", timeout: step.timeoutMs || context.timeoutMs });
      return { ok: true, detail: `waitForSelector ${step.selector}` };
    }
    case "waitForText": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      await page.waitForFunction(
        ({ selector, expected, matchMode }) => {
          const el = document.querySelector(selector);
          if (!el) return false;
          const text = (el.innerText || el.textContent || "").trim();
          return matchMode === "contains" ? text.includes(expected) : text === expected;
        },
        {
          selector: step.selector,
          expected: String(step.text ?? ""),
          matchMode: step.contains ? "contains" : "exact",
        },
        { timeout: step.timeoutMs || context.timeoutMs }
      );
      return { ok: true, detail: `waitForText ${step.selector}` };
    }
    case "waitForURL": {
      const expected = normalizeUrl(step.url, context.baseUrl);
      await page.waitForURL(expected, { timeout: step.timeoutMs || context.timeoutMs });
      context.currentUrl = page.url();
      return { ok: true, detail: `waitForURL ${expected}` };
    }
    case "assertText": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      const actual = await getText(locator);
      const expected = String(step.text ?? "").trim();
      const pass = step.contains ? actual.includes(expected) : actual === expected;
      if (!pass) {
        throw new Error(`assertText failed for ${step.selector}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
      }
      return { ok: true, detail: `assertText ${step.selector}` };
    }
    case "assertVisible": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      const visible = await locator.isVisible({ timeout: step.timeoutMs || context.timeoutMs });
      if (!visible) {
        throw new Error(`assertVisible failed for ${step.selector}`);
      }
      return { ok: true, detail: `assertVisible ${step.selector}` };
    }
    case "assertValue": {
      const locator = locatorFor(page, step.selector, context.timeoutMs);
      const actual = await locator.inputValue({ timeout: step.timeoutMs || context.timeoutMs });
      const expected = String(step.value ?? "");
      if (actual !== expected) {
        throw new Error(`assertValue failed for ${step.selector}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
      }
      return { ok: true, detail: `assertValue ${step.selector}` };
    }
    case "sleep": {
      await page.waitForTimeout(step.ms || 250);
      return { ok: true, detail: `sleep ${step.ms || 250}` };
    }
    case "screenshot": {
      const baseName = sanitizeName(step.name || `shot-${String(context.screenshots.length).padStart(2, "0")}`);
      const outPath = path.join(context.outDir, `${baseName}.png`);
      if (step.selector) {
        const locator = locatorFor(page, step.selector, context.timeoutMs);
        await locator.screenshot({ path: outPath, timeout: step.timeoutMs || context.timeoutMs });
      } else {
        await page.screenshot({ path: outPath, fullPage: Boolean(step.fullPage) });
      }
      context.screenshots.push(outPath);
      return { ok: true, detail: `screenshot ${path.basename(outPath)}` };
    }
    default:
      throw new Error(`Unsupported op: ${op}`);
  }
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(args.screenshotDir);
  ensureDir(outDir);
  clearManagedArtifacts(outDir);

  const steps = loadSteps(args);
  const tracker = new EventTracker();
  let runtimeResolution;

  try {
    runtimeResolution = resolvePlaywrightRuntime({ runtimeDir: args.runtimeDir });
  } catch (error) {
    writeBootstrapError(outDir, "playwright-import", error, {
      candidates: buildRuntimeCandidates({ runtimeDir: args.runtimeDir }),
    });
    throw error;
  }

  const { playwright, runtimeInfo, candidates } = runtimeResolution;

  let browser;
  try {
    browser = await launchChromium(playwright, runtimeInfo, args);
  } catch (error) {
    writeBootstrapError(outDir, "chromium-launch", error, {
      runtime: runtimeInfo,
      candidates,
    });
    throw error;
  }

  const page = await browser.newPage({
    viewport: { width: args.viewportWidth, height: args.viewportHeight },
  });
  tracker.attach(page);
  page.setDefaultTimeout(args.timeoutMs);

  const context = {
    baseUrl: args.url,
    currentUrl: args.url,
    outDir,
    timeoutMs: args.timeoutMs,
    screenshots: [],
    stepResults: [],
  };

  try {
    const firstOp = steps[0]?.op;
    if (firstOp !== "goto") {
      await page.goto(args.url, { waitUntil: "domcontentloaded", timeout: args.timeoutMs });
    }

    for (let index = 0; index < steps.length; index++) {
      const step = steps[index];
      const startedAt = new Date().toISOString();
      try {
        const result = await executeStep(page, step, context);
        context.stepResults.push({ index, op: step.op, startedAt, status: "ok", detail: result.detail });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        const failureShot = path.join(outDir, `failure-step-${String(index).padStart(2, "0")}.png`);
        try {
          await page.screenshot({ path: failureShot, fullPage: true });
          context.screenshots.push(failureShot);
        } catch {
          // ignore screenshot failure, original error is more important
        }
        context.stepResults.push({ index, op: step.op, startedAt, status: "failed", error: errorMessage });
        throw error;
      }
    }

    const summary = {
      targetUrl: args.url,
      finalUrl: page.url(),
      outDir,
      runtime: runtimeInfo,
      screenshots: context.screenshots,
      steps: context.stepResults,
      errors: tracker.toJSON(),
    };
    fs.writeFileSync(path.join(outDir, "summary.json"), JSON.stringify(summary, null, 2));

    if (tracker.hasErrors() && !args.allowErrors) {
      const combined = [
        ...tracker.consoleErrors.map((entry) => `console.error: ${truncate(entry.text)}`),
        ...tracker.pageErrors.map((entry) => `pageerror: ${truncate(entry.text)}`),
        ...tracker.requestFailures.map((entry) => `requestfailed: ${truncate(entry.url)} ${truncate(JSON.stringify(entry.failure || {}), 200)}`),
      ];
      throw new Error(`Browser run completed but captured runtime errors:\n${combined.join("\n")}`);
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exit(1);
});
