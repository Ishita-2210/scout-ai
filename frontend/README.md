# Scout frontend

React + TypeScript + Vite support workspace. See [the root README](../README.md) for backend setup, Groq credentials, environment settings, testing and deployment.

```sh
npm ci
npm run dev       # Vite proxies /api to http://127.0.0.1:8000
npm run lint
npm run typecheck
npm run build
npx playwright install chromium
npm test          # Builds then tests the real API with mocked external Groq HTTP
```

Production assets are served by FastAPI on the same origin. `npm run preview` previews static assets only; it is not the full production application. No provider keys belong in this package.
