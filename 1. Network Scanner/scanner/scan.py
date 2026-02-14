import socket
import threading
import uuid
import time
from queue import Queue

from .banner import grab_banner
from .service import detect_service
from db.db import save_results


def run_scan(target, start_port=1, end_port=1024, threads=100):
    queue = Queue()
    open_ports = {}

    # Generate unique scan ID
    scan_id = str(uuid.uuid4())[:8]

    start_time = time.time()

    def scan_port():
        while not queue.empty():
            port = queue.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target, port))

                banner = grab_banner(s, target, port)
                service = detect_service(port, banner)

                print(f"[+] Port {port} ({service}) OPEN -> {banner}")

                open_ports[port] = {
                    "service": service,
                    "banner": banner
                }

                save_results(scan_id, target, port, service, banner)

                s.close()
            except:
                pass
            queue.task_done()

    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(threads):
        t = threading.Thread(target=scan_port, daemon=True)
        t.start()

    queue.join()

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    return scan_id, open_ports, duration
