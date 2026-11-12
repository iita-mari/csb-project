CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    comment_text TEXT
);

CREATE TABLE items (
	id INTEGER PRIMARY KEY,
	title TEXT,
    min_players INTEGER,
    max_players INTEGER,
    age_recommendation TEXT,
    duration TEXT,
    difficulty_level TEXT,
    rating TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);

CREATE INDEX idx_items ON items (user_id);