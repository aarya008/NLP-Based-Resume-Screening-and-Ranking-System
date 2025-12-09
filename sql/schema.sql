-- Database schema for Automated Resume Screening Bot
-- This is written for SQLite but is close to generic SQL.

CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    skills TEXT,
    experience INTEGER,
    score REAL,
    resume_path TEXT
);

CREATE TABLE IF NOT EXISTS job_description (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    required_skills TEXT
);
