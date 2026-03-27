import process from "node:process";
import { resolvePlaywrightRuntime } from "./playwright_runtime.mjs";

function parseArgs(argv) {
  const args = {
    runtimeDir: null,
  };

  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === "--runtime-dir" && next) {
      args.runtimeDir = next;
      i++;
    }
  }

  return args;
}

function main() {
  const args = parseArgs(process.argv);
  const { playwright, runtimeInfo, candidates } = resolvePlaywrightRuntime({
    runtimeDir: args.runtimeDir,
  });

  console.log(
    JSON.stringify(
      {
        runtime: runtimeInfo,
        executablePath: playwright.chromium.executablePath(),
        candidates,
      },
      null,
      2
    )
  );
}

main();
