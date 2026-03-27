CREATE TABLE IF NOT EXISTS achievements (
    id SERIAL PRIMARY KEY,
    entity_type_id INTEGER NOT NULL REFERENCES entity_types(id),
    name TEXT NOT NULL,
    emoji TEXT NOT NULL,
    threshold INTEGER NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_achievements_entity_type_id ON achievements(entity_type_id);

CREATE TABLE IF NOT EXISTS user_achievements (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    achievement_id INTEGER NOT NULL REFERENCES achievements(id),
    achieved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);

INSERT INTO achievements (entity_type_id, name, emoji, threshold, sort_order)
VALUES
    ((SELECT id FROM entity_types WHERE slug = 'girl'), 'Первый шаг', '👋', 1, 1),
    ((SELECT id FROM entity_types WHERE slug = 'girl'), 'Разгон', '🔥', 5, 2),
    ((SELECT id FROM entity_types WHERE slug = 'girl'), 'Десятка', '⭐', 10, 3),
    ((SELECT id FROM entity_types WHERE slug = 'girl'), 'Мастер', '💪', 25, 4),
    ((SELECT id FROM entity_types WHERE slug = 'girl'), 'Легенда', '👑', 50, 5),
    ((SELECT id FROM entity_types WHERE slug = 'beautiful_girl'), 'Ценитель', '💎', 1, 1),
    ((SELECT id FROM entity_types WHERE slug = 'beautiful_girl'), 'Коллекционер', '🌟', 3, 2),
    ((SELECT id FROM entity_types WHERE slug = 'beautiful_girl'), 'Знаток', '🏆', 5, 3),
    ((SELECT id FROM entity_types WHERE slug = 'beautiful_girl'), 'Эксперт', '💫', 10, 4),
    ((SELECT id FROM entity_types WHERE slug = 'beautiful_girl'), 'Легенда красоты', '👑', 25, 5)
ON CONFLICT DO NOTHING;
