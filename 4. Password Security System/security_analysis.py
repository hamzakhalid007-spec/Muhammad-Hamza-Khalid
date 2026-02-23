import hashlib
import bcrypt
import time
from database import get_connection

def compare_algorithms(password):
    conn = get_connection()
    cursor = conn.cursor()

    # MD5
    start = time.time()
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    md5_time = time.time() - start

    # SHA256
    start = time.time()
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    sha256_time = time.time() - start

    # bcrypt
    start = time.time()
    bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    bcrypt_time = time.time() - start

    print("\n--- Hashing Time Comparison ---")
    print(f"MD5 Time: {md5_time}")
    print(f"SHA256 Time: {sha256_time}")
    print(f"bcrypt Time: {bcrypt_time}")

    cursor.execute(
        "INSERT INTO security_logs (algorithm, hash_time, verify_time) VALUES (%s, %s, %s)",
        ("MD5", md5_time, 0)
    )
    cursor.execute(
        "INSERT INTO security_logs (algorithm, hash_time, verify_time) VALUES (%s, %s, %s)",
        ("SHA256", sha256_time, 0)
    )
    cursor.execute(
        "INSERT INTO security_logs (algorithm, hash_time, verify_time) VALUES (%s, %s, %s)",
        ("bcrypt", bcrypt_time, 0)
    )

    conn.commit()
    conn.close()