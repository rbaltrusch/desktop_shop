DROP TABLE IF EXISTS detailed_transactions;

CREATE TABLE detailed_transactions (
    transaction_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (transaction_id)
        REFERENCES transactions (transaction_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT)
