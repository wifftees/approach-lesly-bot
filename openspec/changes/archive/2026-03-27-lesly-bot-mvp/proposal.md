## Why

Нужен Telegram бот для учёта подходов к девушкам и сбора контактов. Цель — соревноваться с друзьями за количество набранных контактов через систему очков и лидерборд. Сейчас учёт ведётся вручную, нет визуализации и мотивации через геймификацию.

## What Changes

- Создание Telegram бота на aiogram 3 с динамической системой сущностей (girl, beautiful_girl, и расширяемой в будущем)
- Каждая сущность имеет свою slash-команду, количество очков, и настройку обязательности контакта — всё хранится в БД
- FSM-flow для добавления записей: запрос контакта с inline-кнопками (Пропустить/Отмена)
- Динамическая ReplyKeyboard, генерируемая из реестра сущностей
- REST API (aiohttp) для Telegram Mini App с валидацией initData
- React Mini App (Mantine UI + Recharts) с лидербордами, просмотром и отправкой контактов
- Полное логирование активности пользователей для будущей аналитики
- Docker + docker-compose для деплоя

## Capabilities

### New Capabilities

- `database-schema`: Схема БД в Supabase — users, entity_types, entries, activity_log. Расширяемый реестр сущностей с динамическими баллами и командами.
- `telegram-bot`: Telegram бот на aiogram 3 — /start, /help, динамические команды из entity_types, FSM для добавления записей, ReplyKeyboard, поздравления.
- `api-server`: REST API на aiohttp — эндпоинты /api/entity-types, /api/stats, /api/contacts, /api/send-contacts. Валидация Telegram initData.
- `mini-app`: React Mini App — вкладки по сущностям, гистограммы лидерборда (Recharts), просмотр и отправка контактов, интеграция с Telegram theme.
- `infrastructure`: Dockerfile (multi-stage), docker-compose, конфигурация через env vars, миграции.

### Modified Capabilities

(нет существующих capabilities)

## Impact

- **Новые зависимости**: aiogram 3, aiohttp, asyncpg, pydantic; React, Mantine, Recharts, Vite
- **Инфраструктура**: Supabase проект (PostgreSQL), VPS с Docker
- **API**: 4 новых REST эндпоинта для Mini App
- **БД**: 4 новых таблицы, 4 индекса, seed-данные для entity_types
- **Telegram**: Регистрация бота, настройка Mini App URL через BotFather
