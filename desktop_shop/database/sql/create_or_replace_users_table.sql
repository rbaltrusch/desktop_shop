DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    dob TEXT CHECK (
        CAST(strftime('%s', join_date)  AS  integer)
        > CAST(strftime('%s', dob)  AS  integer)
    ),
    email_address TEXT NOT NULL UNIQUE COLLATE NOCASE,
    join_date TEXT NOT NULL,
    pw_salt NOT NULL,
    pw_hash NOT NULL,
    hash_function NOT NULL CHECK (email_address LIKE '%_@_%._%')
);

DROP INDEX IF EXISTS idx_user_id;
CREATE INDEX idx_user_id ON users(user_id);
