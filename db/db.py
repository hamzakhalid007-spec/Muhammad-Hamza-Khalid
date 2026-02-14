import mysql.connector
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "muhammad-hamza-khalid",
    "password": "hamza000",
    "database": "network_scanner",
    "autocommit": True
}


def save_results(scan_id, target, port, service, banner):
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        query = """
            INSERT INTO scan_results 
            (scan_id, scan_time, target_ip, port, service, banner)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                scan_id,
                datetime.now(),
                target,
                port,
                service,
                banner
            )
        )

        cursor.close()
        db.close()

    except Exception as e:
        print(f"[DB ERROR] {e}")
