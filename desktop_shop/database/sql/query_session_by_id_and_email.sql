SELECT session_id FROM sessions
WHERE session_id = ?
AND user_id IN
    (
        SELECT user_id FROM users
        WHERE email_address = ?
    )
