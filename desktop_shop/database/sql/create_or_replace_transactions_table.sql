DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date TEXT,
    cost REAL NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

DROP INDEX IF EXISTS idx_user_id;
CREATE INDEX idx_user_id ON transactions(user_id);
