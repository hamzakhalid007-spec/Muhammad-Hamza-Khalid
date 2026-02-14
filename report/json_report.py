import json
import os


def save_json_report(scan_id, target, results, duration):
    os.makedirs("report", exist_ok=True)

    filename = f"report/scan_{scan_id}.json"

    data = {
        "scan_id": scan_id,
        "target": target,
        "duration_seconds": duration,
        "open_ports": results
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[+] JSON report saved: {filename}")
