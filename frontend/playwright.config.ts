import { defineConfig } from "@playwright/test";
import process from "node:process";
export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  workers: 1,
  use: { baseURL: "http://127.0.0.1:8765", trace: "retain-on-failure" },
  webServer: {
    command: `${process.env.SCOUT_PYTHON || (process.platform === "win32" ? ".venv\\Scripts\\python.exe" : ".venv/bin/python")} -m uvicorn backend.tests.browser_app:app --host 127.0.0.1 --port 8765`,
    cwd: "..",
    url: "http://127.0.0.1:8765/health",
    reuseExistingServer: false,
    timeout: 60000,
  },
});
