CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_input TEXT NOT NULL,
    perception_emotion TEXT,
    perception_intent TEXT,
    goal TEXT,
    reply TEXT,
    mood REAL,
    empathy REAL,
    directness REAL,
    caution REAL
);