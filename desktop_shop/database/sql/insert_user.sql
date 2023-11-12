INSERT INTO users (
    first_name,
    last_name,
    gender,
    dob,
    email_address,
    join_date,
    pw_salt,
    pw_hash,
    hash_function
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
