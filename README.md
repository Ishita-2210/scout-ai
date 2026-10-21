# Scout AI

Scout helps displaced students and families continue their education. It provides guidance on schools and admissions, scholarships, replacing documents, temporary housing, education rights, and learning wellbeing.

The application uses React 19, TypeScript, Vite and Tailwind on the frontend; FastAPI, SQLAlchemy and SQLite on the backend. All LLM calls run server-side through the official Groq Python SDK. The original six specialist prompts and domain schemas are retained.

## Request flow

```text
React support workspace
        |
FastAPI: signed session, validation, request ledger
        |
Groq root orchestrator (all relevant domains)
        |
Schools | Scholarships | Documents | Housing | Rights | Wellbeing
        |
Optional Serper search + read-only bundled PDF references
        |
Validated structured results + SQLite conversation/profile storage
        |
Readable answer, source links, saved history
```

## What works

- A responsive support workspace with six starting topics, multiline messages, copyable answers, expandable structured results, source links, and clear loading/error states.
- Anonymous, signed browser sessions with owned conversation history, reload, deletion, and removal of remembered profile data. No account registration or cross-device login is implemented.
- Groq routing selects every relevant specialist. Each specialist returns validated JSON. Answers are combined without another model call. A simple question normally takes one routing call plus one specialist call; multi-topic questions cost more.
- Bounded recent history and explicitly stated profile facts provide context across turns. Profile extraction shares the routing call.
- Read-only retrieval of relevant text from bundled PDFs. Optional Serper web search supplies current sources. Search failures are clearly marked; Scout must not invent current recommendations when sources are unavailable.
- Input limits, durable duplicate-request protection, concurrency limits, cancellation, timeout handling, bounded transient retries, and distinct quota/configuration errors.

Scout provides guidance, not official admission decisions, professional legal advice, or clinical care. Confirm changing details with official sources. There is no file-upload, vision, audio, or streaming chat feature in this repository.

## Local setup

Prerequisites: Python 3.11+ (verified with 3.13), Node.js 22.12+ and npm. Run backend commands from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements-dev.txt
```

On macOS/Linux, activate with `source .venv/bin/activate` instead. A fresh environment avoids conflicts with obsolete Google ADK dependencies in older environments.

Create `.env` from [.env.example](.env.example) **only if you do not already have one**. Keep existing values you still need. Never add `.env` to Git.

1. Create a key at [Groq Console → API keys](https://console.groq.com/keys).
2. Set `GROQ_API_KEY` in the root `.env`.
3. Generate a session secret with `python -c "import secrets; print(secrets.token_hex(32))"` and set `SESSION_SECRET`. Keep it stable so browser sessions survive restarts.
4. Optionally set `SERPER_API_KEY` for current web results. Without it, general guidance and local PDF references remain available, with explicit verification warnings.

Start the API:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` and `/health` to the backend. No frontend API key or provider configuration is needed. The API can start without a Groq key, but the interface disables chat and explains that setup is required.

## Environment reference

All settings below belong to the **backend**. Never use a `VITE_` prefix for credentials.

| Variable | Default | Purpose |
| --- | --- | --- |
| `GROQ_API_KEY` | empty | Required to generate answers. |
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Model supporting strict JSON Schema output. |
| `SESSION_SECRET` | temporary development secret | Use a stable random secret of at least 32 characters. |
| `SECURE_COOKIES` | `false` | Set `true` behind HTTPS in production; then a valid session secret is required at startup. |
| `ALLOWED_ORIGINS` | localhost and 127.0.0.1 on port 5173 | Comma-separated browser origins, including scheme and port; no wildcard. |
| `SERPER_API_KEY` | empty | Optional current web search. Search terms are sent to Serper. |
| `DATABASE_URL` | root `scout.db` | SQLAlchemy database URL. SQLite needs a persistent writable disk. |
| `AI_TIMEOUT` | `30` seconds | Timeout for each provider HTTP request, range 1–120. |
| `CHAT_TIMEOUT` | `120` seconds | Overall turn deadline including queueing and search, range 5–300. The browser stops waiting after 125 seconds. |
| `AI_MAX_TOKENS` | `2048` | Completion budget per model call, range 256–8192. |
| `AI_CONCURRENCY` | `2` | Concurrent provider calls per process, range 1–10. |
| `CHAT_REQUESTS_PER_MINUTE` | `10` | Per-session sliding window. The IP allowance is three times this. |

Groq's [production model list](https://console.groq.com/docs/models) and [strict structured-output support](https://console.groq.com/docs/structured-outputs) were checked on October 21, 2026. `openai/gpt-oss-20b` was selected for fast routing and text guidance with validated structured results. Its provider is Groq even though the model ID contains `openai/`. Requests go to `https://api.groq.com/openai/v1/chat/completions`. The Groq SDK 1.x is configured with the host `https://api.groq.com` because it appends `/openai/v1` itself; the full `/openai/v1` base URL is for OpenAI-compatible clients. Check current availability and your account's model permissions before overriding the model.

## Checks

From the root, in the activated environment:

```powershell
python -m pytest -q
python -m ruff check backend
python -m ruff format --check backend
python -m compileall -q backend
python -m pip check
```

From `frontend`:

```powershell
npm run lint
npm run typecheck
npm run build
npx playwright install chromium
npm test
npm audit
```

`npm test` builds production assets, starts an isolated FastAPI test server, and runs Chromium journeys against real routes, persistence, and Groq SDK response validation. Only the external Groq HTTP transport is mocked. Tests also cover onboarding, mobile navigation, keyboard focus, copy, reload/deletion, missing setup, cancellation and rate-limit messaging. The desktop onboarding includes an axe WCAG A/AA scan. Screenshots are written to `artifacts/`.

Playwright defaults to the root `.venv` interpreter. To use another environment in PowerShell, set `$env:SCOUT_PYTHON='.venv-scout\Scripts\python.exe'` before `npm test`. On Linux use `SCOUT_PYTHON=.venv-scout/bin/python npm test`. No real AI quota is used. Tests create temporary databases and never touch your `scout.db`.

For formatting frontend source, run `npx prettier --write src tests playwright.config.ts vite.config.ts`.

## Production deployment

The supported architecture is **one FastAPI process serving the built React app on the same origin**, with a persistent SQLite disk. This keeps HttpOnly cookies and API requests on the same origin.

```powershell
cd frontend
npm ci
npm run build
cd ..
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 1
```

Serve HTTPS through your hosting platform or reverse proxy. Configure `GROQ_API_KEY`, a stable `SESSION_SECRET`, `SECURE_COOKIES=true`, your exact HTTPS `ALLOWED_ORIGINS`, and a persistent `DATABASE_URL` in the host's secret/environment settings. Keep secrets out of Docker images and frontend builds. Health checks use `/health`; API documentation is at `/docs`.

Alternatively use the included Dockerfile:

```sh
docker build -t scout-ai .
docker run --rm --env-file .env -p 8000:8000 -v scout-data:/data scout-ai
```

For a local HTTP Docker smoke test use `SECURE_COOKIES=false`. For production terminate HTTPS and set it to `true`. The image defaults to `/data/scout.db` and runs as a non-root user. The Docker recipe is provided for deployment; it has not been built in this workspace.

Back up the existing database before deployment. Startup adds missing tables, including the request ledger, using SQLAlchemy `create_all`; it does not drop or rewrite existing data. There were no migrations in the original repository. Future changes to existing table columns need an explicit migration. Old shared `test_user` conversations remain in the database and are not exposed to new anonymous sessions.

Run **one worker / one replica** with SQLite and the in-process admission/rate limits. Before scaling publicly, add a shared ingress rate limiter (including session creation), trusted proxy IP configuration, and shared coordination/storage. Otherwise per-process quotas can be bypassed across replicas. The app admits at most eight active turns per process and one per session. These controls reduce abuse; they do not make Groq unlimited.

The original repository already tracks `scout.db` and a Chroma SQLite index. These files are preserved, and new runtime databases are ignored. `.gitignore` cannot untrack existing files: do not include those tracked runtime databases in a public release. Move production data to the configured persistent volume and review tracked data before publishing. Do not rewrite repository history to hide data or credentials.

## Failure behavior and troubleshooting

| Symptom | Action |
| --- | --- |
| Setup needed | Set `GROQ_API_KEY` in the backend environment and restart it. |
| AI credentials need attention | Replace an invalid/revoked key; verify Groq project/model permissions. The browser never receives the key or provider error body. |
| Model configuration needs attention | Check the current supported model list and strict JSON support. Update `GROQ_MODEL` server-side. |
| Rate limit / wait countdown | Respect the displayed delay and review [your Groq limits](https://console.groq.com/settings/limits). Limits apply to the organization and model, including tokens. |
| Daily quota exhausted | Wait for the provider's reset or change the account plan. Automatic retries stop. If no reset header is supplied, Scout applies a conservative one-hour cooldown. |
| Provider unavailable | Transient 429/500/502/503/504 responses receive at most two retries with jitter. Waits longer than eight seconds are returned to the browser instead. |
| Timeout / stopped request | Check saved conversation history before explicitly retrying. Timeouts and ambiguous connection failures are not automatically replayed; cancellation cannot undo a request already processed by the provider. |
| Request already processing/interrupted | The durable ledger prevents replay of that request ID. Check history; an explicit retry creates a new request ID. This may consume quota again. |
| Unreadable/incomplete answer | Malformed, schema-invalid, empty or truncated output is rejected. Try a shorter question; do not increase output limits indiscriminately. |
| Live search unavailable | Check the optional Serper key/service. Current recommendations must be confirmed externally; no synthetic results are substituted. |
| Session expired / missing history | Refresh to create a session. Keep `SESSION_SECRET` stable and use the same browser. Clearing cookies or expiry after 30 days prevents access to old anonymous history. |
| Cookie does not persist | Match hostname/origin and use HTTPS when secure cookies are enabled. Keep the browser and API on the same origin. |

Provider rate/reset headers, including `Retry-After`, remaining daily requests and remaining minute tokens, are interpreted server-side. Successful responses that exhaust a limit also activate the cooldown. See [Groq rate-limit documentation](https://console.groq.com/docs/rate-limits).

Logs contain generated request IDs, latency, HTTP status and failure categories, without prompts, search queries, API keys or raw provider errors. The response's `X-Request-ID` can be used to correlate an error with logs. Configure retention/backups appropriately for stored student conversations. Delete-all removes active session data; it does not erase your infrastructure backups or provider records.

## Optional legacy semantic index

The previously disconnected Chroma/Gemini embedding utilities are retained for offline indexing of existing knowledge, separately from live chat. Groq does not provide an embedding endpoint, so they have **not** been pointed at a text-generation model. Live chat uses local PDF text retrieval and requires no Google key, vector download or Chroma migration.

If you deliberately use the old semantic tooling:

```powershell
python -m pip install -r backend/requirements-rag.txt
python -m backend.rag.indexer
```

Set optional server-side `GOOGLE_API_KEY` and `EMBEDDING_MODEL=gemini-embedding-001`. Indexing consumes Google embedding quota. Back up `backend/data/chroma` first. This optional external-service path is not part of the live Groq verification and needs its own credentials. Existing vectors are preserved.

## Live verification still required

With your real Groq key configured, ask a wellbeing question, then a multi-topic question with a city/grade; confirm structured sections and follow-up context. With Serper configured, check that school or scholarship searches return current source links. Restart the backend and verify history with the same session secret. Confirm HTTPS cookies and persistent-disk backups in your chosen host. Automated tests mock providers and do not establish live account access, current recommendation accuracy, or deployment availability.
