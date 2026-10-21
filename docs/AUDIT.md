# Scout improvement pass — October 21, 2026

## Original findings

- React/Vite/TypeScript frontend and FastAPI/Python backend; Gemini via Google ADK routed to six specialists. There was no working account login, upload, vision, audio or streaming journey.
- The chat endpoint constructed a new runner and in-memory session service for every turn. The browser sent the same hardcoded user/session IDs for everyone; no authorization boundary protected stored conversations.
- Specialist output schemas were commented out. The API sometimes returned JSON objects while the frontend declared and rendered strings.
- API requests had no message/body limits, durable idempotency, application quota controls, cancellation or safe provider-specific error handling. Runtime exception strings could reach users.
- Environment imports required both Google and Serper credentials even for startup. The requirements file omitted SQLAlchemy and dependencies used by the unused PDF/vector pipeline.
- PDF RAG was not connected to chat. Its result construction used fields the models did not accept; embedding initialization required credentials at import time. Memory extraction returned no values and profiles were only in memory.
- The interface had fake recent chats, a fixed student name, broken logo paths, an unverified online label, inactive navigation/actions, and no working history, retry or deletion flow.
- No automated test suite or root setup/deployment README existed. The original frontend lint/build passed, and the backend imported in the already populated environment.
- Existing unrelated working-tree changes: `scout.db` and a trailing blank line in `frontend/index.html`. Database data was preserved. The HTML was updated for Scout metadata while retaining the extra trailing line.

## Completed checklist

- [x] Inspect source, domain schemas, all specialist prompts, database and memory layers, search, PDF/vector tooling, frontend components, manifests and configuration.
- [x] Preserve the stack, six support domains, existing prompts, domain models, knowledge PDFs and existing database/index files.
- [x] Replace Gemini/ADK text generation with a centralized official Groq SDK service and configurable `openai/gpt-oss-20b` default, checked against current Groq docs.
- [x] Enforce JSON schema generation and independent Pydantic validation, including malformed/truncated response handling.
- [x] Bound retries, input/body/history/output size, concurrency, active turns and per-session/IP requests; respect provider retry/reset headers and daily exhaustion.
- [x] Prevent automatic replay after ambiguous timeouts/disconnects. Persist request IDs and completed results transactionally with successful conversation turns.
- [x] Add signed HttpOnly anonymous sessions, ownership checks, exact CORS/origin rules, safe errors, security headers and sanitized logs.
- [x] Persist explicitly stated profile facts using the existing memory table without another LLM call. Remove the no-op memory extractor and unused school search placeholders.
- [x] Connect bounded read-only local PDF retrieval. Preserve optional Google embedding/Chroma utilities separately without pretending Groq provides embeddings.
- [x] Rebuild onboarding, navigation, actual history, chat input and result presentation; support copy/retry/stop/new/delete controls and confirmed deletion of all session data.
- [x] Verify mobile/desktop layouts, keyboard navigation, production assets, privacy controls and accessibility contrast.
- [x] Update requirements, root/frontend READMEs, environment example, ignores, production static hosting and non-root Docker recipe.

## Main modules

- `backend/services/ai_service.py`: Groq integration and failure policy.
- `backend/execution/runner.py`, `backend/agents/*`: retained specialist definitions, routing, parallel domain work, validated results and bounded history.
- `backend/api/chat.py`, `backend/api/security.py`, `backend/schemas/*`: browser sessions, contracts, ownership, limits and history/data APIs.
- `backend/database/models.py`, `backend/memory/*`: additive request ledger and persisted profiles, preserving existing tables/data.
- `backend/services/knowledge_service.py`, `backend/services/search_service.py`: local PDF context and optional live web results.
- `frontend/src/pages/ChatPage.tsx`, `frontend/src/components/*`, `frontend/src/services/api.ts`, `frontend/src/index.css`: redesigned workspace and real interactions.
- `backend/tests/*`, `frontend/tests/*`: isolated unit/integration/browser verification.

API v2 replaces the old client-supplied `user_id` contract. `POST /api/session` establishes a signed cookie. `POST /api/chat` accepts UUID `session_id`, UUID `request_id`, and `message`; returns a typed `response` containing text, structured sections, sources, references and warnings. Third-party API clients must adopt the new contract and retain cookies.

## Verification and limits

- Backend: 36 tests pass in a fresh `.venv-scout` installed from the documented requirements. Ruff checks/formatting, Python compilation and `pip check` pass.
- Frontend: ESLint, TypeScript and production Vite build pass. npm audit reports zero vulnerabilities after removing unused Axios/Router and updating vulnerable compatible transitive dependencies.
- Eight Chromium journeys pass against the real FastAPI routes and temporary SQLite database, with external Groq HTTP mocked. Tests include real SDK parsing, persistence/reload/deletion, duplicate submission prevention, cancellation, setup errors and quota messages. Axe scans pass for desktop onboarding, mobile onboarding and the privacy dialog.
- The existing database was upgraded on an isolated copy; all existing row counts were retained and the original database's hash was unchanged by that check.
- Configured local secret values were checked against repository files and generated frontend assets: no matches. `.env` is not tracked. Existing tracked database/index files are still present and require review before any public release.
- No `GROQ_API_KEY` is configured locally. Live Groq account access/model quality, Serper service behavior, optional Google embedding calls and a deployed host remain unverified. Tests never use real provider quota.
- Docker is unavailable in this workspace. The Dockerfile is supplied but its image has not been built here.
- The supported deployment is one worker/replica with persistent SQLite. Shared ingress quotas/coordination are required before scaling. Anonymous browser identity is not an account recovery or cross-device authentication system.
- The old `.venv` retains an unrelated Google ADK/OpenTelemetry dependency conflict. The verified fresh `.venv-scout` is clean; the obsolete ADK dependency is absent from the application requirements.

Required operator actions: configure server-side Groq/session settings, optionally Serper, and choose HTTPS hosting with a persistent disk. Follow the root README's live verification and public-release data review instructions. No deployment or repository push was performed.

Git whitespace review reports only the pre-existing trailing blank line retained in frontend/index.html. No new whitespace errors were introduced.

## Follow-up: live Groq URL correction

With credentials configured, live requests exposed a client-initialization defect: Groq SDK 1.7 appends `/openai/v1` itself, so supplying the OpenAI-compatible base URL duplicated that path and returned `404 unknown_url`. The SDK now receives `https://api.groq.com`. Production initialization and the browser transport mock both assert the exact completion endpoint. The earlier mocks injected an SDK client using its default URL and missed this production-only difference.

Verification after correction: 37 backend tests and eight browser journeys pass. A real Groq structured routing request succeeded, and the restarted application on port 8000 returned HTTP 200 with the expected school/location clarification. The temporary diagnostic session was removed. Live model quality for every specialist and deployment hosting remain outside this check.
