CREATE TABLE visits(
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE recipes(
    id INTEGER PRIMARY KEY,
    title TEXT,
    ingredients TEXT,
    instructions TEXT,
    status INTEGER DEFAULT 1,
    date TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE tags(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE recipe_tags(
    recipe_id INTEGER REFERENCES recipes,
    tag_id INTEGER REFERENCES tags
);