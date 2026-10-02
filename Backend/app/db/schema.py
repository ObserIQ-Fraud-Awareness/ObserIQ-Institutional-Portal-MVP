import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS tenants (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    subdomain       TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    contract_tier   TEXT NOT NULL DEFAULT 'trial',
    default_locale  TEXT NOT NULL DEFAULT 'en',
    logo_url        TEXT,
    primary_color   TEXT,
    secondary_color TEXT,
    contact_email   TEXT,
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS locales (
    code   TEXT PRIMARY KEY,
    name   TEXT NOT NULL,
    is_rtl INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS localized_strings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    locale_code  TEXT NOT NULL REFERENCES locales(code),
    string_key   TEXT NOT NULL,
    string_value TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (locale_code, string_key)
);


CREATE TABLE IF NOT EXISTS leads (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id         INTEGER REFERENCES tenants(id),
    institution_type  TEXT,
    org_name          TEXT NOT NULL,
    contact_name      TEXT NOT NULL,
    contact_email     TEXT NOT NULL,
    contact_role      TEXT,
    risk_score        INTEGER,
    risk_category     TEXT,
    locale_code       TEXT REFERENCES locales(code),
    report_sent       INTEGER NOT NULL DEFAULT 0,
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get_db():
    """
    Open a new DB connection for this request if it doesn't exist,
    and reuse it for the rest of the request via Flask's `g` object.
    """
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close the DB connection at the end of the request, if one was opened.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Create all tables if they don't exist yet.
    """
    db = get_db()
    db.executescript(SCHEMA)