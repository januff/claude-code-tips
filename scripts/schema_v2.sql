-- Claude Code Tips Schema v2
-- Created: 2026-01-02
-- Features: Reply threading, media tracking, link resolution, FTS

CREATE TABLE IF NOT EXISTS tweets (
    id TEXT PRIMARY KEY,
    handle TEXT NOT NULL,
    display_name TEXT,
    text TEXT NOT NULL,
    url TEXT NOT NULL,
    posted_at TEXT,
    
    -- Metrics
    replies INTEGER DEFAULT 0,
    reposts INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    bookmarks INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    quotes INTEGER DEFAULT 0,
    engagement_score INTEGER DEFAULT 0,
    
    -- Threading
    conversation_id TEXT,
    is_reply INTEGER DEFAULT 0,
    in_reply_to_id TEXT,
    in_reply_to_user TEXT,
    reply_depth INTEGER DEFAULT 0,
    
    -- Source tracking
    source TEXT NOT NULL,
    extracted_at TEXT NOT NULL,
    
    -- Card/link preview
    card_url TEXT,
    card_title TEXT,
    card_description TEXT,
    
    -- Raw data
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT NOT NULL REFERENCES tweets(id),
    media_type TEXT NOT NULL,  -- 'image', 'video', 'gif'
    url TEXT NOT NULL,
    expanded_url TEXT,
    alt_text TEXT,
    video_url TEXT,
    local_path TEXT,
    downloaded_at TEXT,
    ocr_text TEXT,
    vision_description TEXT,
    analyzed_at TEXT,
    is_settings_screenshot INTEGER DEFAULT 0,
    is_code_screenshot INTEGER DEFAULT 0,
    extracted_commands TEXT  -- JSON array
);

CREATE INDEX IF NOT EXISTS idx_media_tweet ON media(tweet_id);

CREATE TABLE IF NOT EXISTS thread_replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_tweet_id TEXT NOT NULL REFERENCES tweets(id),
    reply_tweet_id TEXT NOT NULL,
    reply_text TEXT NOT NULL,
    reply_author_handle TEXT,
    reply_author_name TEXT,
    reply_posted_at TEXT,
    reply_likes INTEGER DEFAULT 0,
    reply_depth INTEGER DEFAULT 1,
    is_author_reply INTEGER DEFAULT 0,
    is_educational INTEGER DEFAULT 0,
    quality_score INTEGER,
    has_media INTEGER DEFAULT 0,
    media_urls TEXT,  -- JSON array
    fetched_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_replies_parent ON thread_replies(parent_tweet_id);

CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT REFERENCES tweets(id),
    short_url TEXT,
    expanded_url TEXT,
    content_type TEXT,  -- 'blog', 'github', 'image', 'video', 'docs'
    title TEXT,
    description TEXT,
    fetched_at TEXT,
    raw_content TEXT
);

CREATE TABLE IF NOT EXISTS tip_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS tips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT UNIQUE REFERENCES tweets(id),
    tip_number INTEGER,
    category TEXT,
    summary TEXT,
    is_curated BOOLEAN DEFAULT 0,
    quality_rating INTEGER,
    key_technique TEXT,
    commands_mentioned TEXT,
    tools_mentioned TEXT,
    settings_from_screenshot TEXT,
    code_snippets TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS sync_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    synced_at TEXT NOT NULL,
    source TEXT NOT NULL,
    source_id TEXT,
    items_processed INTEGER,
    items_new INTEGER,
    items_updated INTEGER,
    media_found INTEGER,
    replies_found INTEGER,
    notes TEXT
);

-- FTS for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS tweets_fts USING fts5(
    id, text, handle, display_name, card_title,
    content='tweets', content_rowid='rowid'
);

-- Trigger to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS tweets_fts_insert AFTER INSERT ON tweets BEGIN
    INSERT INTO tweets_fts(rowid, id, text, handle, display_name, card_title)
    VALUES (new.rowid, new.id, new.text, new.handle, new.display_name, new.card_title);
END;

-- Seed categories
INSERT OR IGNORE INTO tip_categories (name, description) VALUES
    ('context', 'Session and context management'),
    ('planning', 'Planning and workflow'),
    ('documentation', 'Documentation and memory'),
    ('skills', 'Custom skills and tools'),
    ('prompting', 'Prompting techniques'),
    ('integration', 'External tool integration'),
    ('subagents', 'Subagents and parallel work'),
    ('code_quality', 'Code quality and review'),
    ('obsidian', 'Obsidian/notes integration'),
    ('voice', 'Voice and TTS integration');
