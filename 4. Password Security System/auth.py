import bcrypt
from database import get_connection
from password_policy import validate_password

def register_user(username, password):
    policy_check = validate_password(password)
    if policy_check != "Valid":
        print(policy_check)
        return

    conn = get_connection()
    cursor = conn.cursor()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
            (username, hashed_password.decode())
        )
        conn.commit()
        print("User registered successfully!")
    except:
        print("Username already exists!")

    conn.close()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT hashed_password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            print("Login successful!")
        else:
            print("Incorrect password!")
    else:
        print("User not found!")

    conn.close()