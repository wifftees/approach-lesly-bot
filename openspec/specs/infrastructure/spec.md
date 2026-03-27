## ADDED Requirements

### Requirement: Multi-stage Dockerfile builds React and runs Python
The Dockerfile SHALL use multi-stage build: stage 1 builds the React Mini App (Node.js), stage 2 copies the built static files into a Python 3.12 runtime with all bot dependencies.

#### Scenario: Docker build produces working image
- **WHEN** `docker build .` is executed
- **THEN** the resulting image contains the Python bot, all dependencies, and the built React Mini App static files

### Requirement: docker-compose defines single service
The docker-compose.yml SHALL define a single `bot` service with port mapping (8080:8080), env_file (.env), and restart policy `unless-stopped`.

#### Scenario: docker-compose up starts the bot
- **WHEN** `docker-compose up -d` is executed with valid .env
- **THEN** the bot starts, connects to Supabase, and serves the API + Mini App on port 8080

### Requirement: Environment configuration via .env
The system SHALL be configured via environment variables: BOT_TOKEN, DATABASE_URL, WEBAPP_URL, API_HOST (default 0.0.0.0), API_PORT (default 8080). A .env.example file SHALL document all required variables.

#### Scenario: Missing required env var
- **WHEN** the bot starts without BOT_TOKEN or DATABASE_URL
- **THEN** the system exits with a clear error message indicating the missing variable

### Requirement: SQL migration file for initial schema
The system SHALL include a migrations/001_initial.sql file containing all CREATE TABLE statements, indexes, and seed data for entity_types.

#### Scenario: Fresh database setup
- **WHEN** the migration SQL is executed against an empty Supabase database
- **THEN** all 4 tables (users, entity_types, entries, activity_log) are created with indexes, and entity_types contains seed data for girl and beautiful_girl

### Requirement: Project structure follows defined layout
The project SHALL follow the directory structure defined in the design document with clear separation: bot/ for Python code, miniapp/ for React code, migrations/ for SQL.

#### Scenario: Project structure is navigable
- **WHEN** a developer opens the project
- **THEN** bot logic is in bot/, Mini App in miniapp/, migrations in migrations/, and infrastructure files (Dockerfile, docker-compose.yml) are at root level
