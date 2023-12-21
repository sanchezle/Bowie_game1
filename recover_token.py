import sqlite3
import random
import os
from werkzeug.security import check_password_hash, generate_password_hash

def process_user_recovery_tokens():
    # Define the database path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "bowiegame.db")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all users
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()

    # Generate tokens and update database
    with open('user_tokens.txt', 'w') as file:
        for user_id, username in users:
            # Generate a 6-digit token
            token = str(random.randint(100000, 999999))

            # Write username and token to the file
            file.write(f"{username}: {token}\n")

            # Hash the token
            hashed_token = generate_password_hash(token)

            # Update the database with the hashed token
            cursor.execute("UPDATE users SET recover_user_token = ? WHERE id = ?", (hashed_token, user_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Example usage
process_user_recovery_tokens()
