SELECT
    first_name,
    last_name,
    gender,
    dob,
    email_address,
    join_date
FROM users
WHERE email_address = ?
