CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_active_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS entity_types (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    command TEXT UNIQUE NOT NULL,
    points INTEGER NOT NULL DEFAULT 1,
    contact_required BOOLEAN NOT NULL DEFAULT FALSE,
    congratulation_texts TEXT[] NOT NULL DEFAULT '{}',
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS entries (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    entity_type_id INTEGER NOT NULL REFERENCES entity_types(id),
    contact_username TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_entries_user_id ON entries(user_id);
CREATE INDEX idx_entries_entity_type_id ON entries(entity_type_id);

CREATE TABLE IF NOT EXISTS activity_log (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    action TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at);

INSERT INTO entity_types (slug, display_name, command, points, contact_required, congratulation_texts, sort_order)
VALUES
    ('girl', 'Девочка', '/add_girl', 2, FALSE,
     ARRAY['Красавчик! +{points} очков 🔥', 'Ещё одна в коллекции! +{points} 💪', 'Машина! Продолжай! +{points} 🚀'],
     1),
    ('beautiful_girl', 'Красивая девочка', '/add_beautiful_girl', 6, TRUE,
     ARRAY['ЛЕГЕНДА! Красотка — это +{points} очков! 🏆', 'Ты МОНСТР! +{points} за красотку! 💎', 'Невероятно! Красотка в кармане — +{points}! 👑'],
     2)
ON CONFLICT (slug) DO NOTHING;
