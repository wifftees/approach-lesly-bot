## 1. Infrastructure & Project Setup

- [x] 1.1 Create project directory structure (bot/, bot/handlers/, bot/services/, bot/api/, miniapp/, migrations/)
- [x] 1.2 Create requirements.txt with dependencies (aiogram==3.x, aiohttp, asyncpg, pydantic, pydantic-settings)
- [x] 1.3 Create .env.example with all required environment variables (BOT_TOKEN, DATABASE_URL, WEBAPP_URL, API_HOST, API_PORT)
- [x] 1.4 Create bot/config.py with pydantic-settings Config class loading env vars
- [x] 1.5 Create migrations/001_initial.sql with all CREATE TABLE statements, indexes, and seed data for entity_types

## 2. Database Layer

- [x] 2.1 Create bot/db.py with asyncpg connection pool (init_db, close_db, get_pool)
- [x] 2.2 Create bot/models.py with pydantic models (User, EntityType, Entry, ActivityLog)
- [x] 2.3 Create bot/services/entity_type.py — load all entity_types, cache in memory, lookup by command/slug
- [x] 2.4 Create bot/services/user.py — upsert user (create or update last_active_at), get user by id
- [x] 2.5 Create bot/services/entry.py — create entry, get entries count by user+entity_type, get contacts by user+entity_type
- [x] 2.6 Create bot/services/activity.py — log activity (insert into activity_log)

## 3. Telegram Bot Core

- [x] 3.1 Create bot/main.py — entry point: init bot, register handlers, start aiohttp + polling
- [x] 3.2 Create bot/keyboards.py — dynamic ReplyKeyboard from entity_types + /stats + /help, inline keyboards for FSM (skip/cancel)
- [x] 3.3 Create bot/handlers/start.py — /start handler (upsert user, welcome message, show keyboard) and /help handler (dynamic command list)
- [x] 3.4 Create bot/handlers/add_entry.py — universal FSM for all entity types: detect entity_type by command, ask contact, handle skip/cancel/input, save entry, send congratulation
- [x] 3.5 Create bot/handlers/stats.py — /stats handler (inline button with WebAppInfo opening Mini App URL)
- [x] 3.6 Register all handlers in bot/handlers/__init__.py, wire dynamic command registration from entity_types

## 4. API Server

- [x] 4.1 Create bot/api/server.py — aiohttp Application setup, startup/shutdown hooks, static file serving for miniapp dist/
- [x] 4.2 Create bot/api/middleware.py — Telegram initData HMAC-SHA256 validation middleware, extract user_id
- [x] 4.3 Create bot/api/handlers.py — GET /api/entity-types handler
- [x] 4.4 Create bot/api/handlers.py — GET /api/stats handler (aggregate entries with points per user per entity_type)
- [x] 4.5 Create bot/api/handlers.py — GET /api/contacts handler (list contacts for user+entity_type)
- [x] 4.6 Create bot/api/handlers.py — POST /api/send-contacts handler (bot sends contacts message to requesting user)
- [x] 4.7 Create bot/api/routes.py — register all routes and middleware

## 5. Mini App (React)

- [x] 5.1 Initialize React project with Vite + TypeScript in miniapp/ directory, install Mantine, Recharts
- [x] 5.2 Create miniapp/src/theme.ts — Telegram WebApp theme integration (themeParams → Mantine theme)
- [x] 5.3 Create miniapp/src/types.ts — TypeScript types for API responses (EntityType, User, Stat, Contact)
- [x] 5.4 Create miniapp/src/api/client.ts — API client with initData header, fetch functions for all endpoints
- [x] 5.5 Create miniapp/src/components/OverallTab.tsx — overall leaderboard bar chart (sorted by total points descending, labels on top)
- [x] 5.6 Create miniapp/src/components/Leaderboard.tsx — reusable bar chart component with Recharts (sorted bars, labels "N pts (K шт)")
- [x] 5.7 Create miniapp/src/components/ContactsList.tsx — contacts list display component
- [x] 5.8 Create miniapp/src/components/EntityTab.tsx — entity tab with leaderboard chart, user dropdown, show/send contacts buttons
- [x] 5.9 Create miniapp/src/App.tsx — main app with Mantine provider, Tabs (dynamic from entity_types), refresh button

## 6. Docker & Deployment

- [x] 6.1 Create Dockerfile — multi-stage: Node.js build for miniapp → Python 3.12 slim runtime with bot + static files
- [x] 6.2 Create docker-compose.yml — single bot service with port 8080, env_file, restart unless-stopped
- [x] 6.3 Create .dockerignore (node_modules, __pycache__, .env, .git)

## 7. Integration & Testing

- [ ] 7.1 End-to-end manual test: /start → /add_girl → skip contact → verify entry in DB
- [ ] 7.2 End-to-end manual test: /add_beautiful_girl → provide contact → verify entry with contact in DB
- [ ] 7.3 End-to-end manual test: /stats → open Mini App → verify leaderboard renders
- [ ] 7.4 End-to-end manual test: Mini App → select user → show contacts → send contacts → verify message received
- [ ] 7.5 Verify dynamic extensibility: INSERT new entity_type → restart bot → verify new command and Mini App tab appear
