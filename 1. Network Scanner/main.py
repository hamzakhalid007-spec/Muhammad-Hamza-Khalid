import argparse
from scanner.scan import run_scan
from report.console import print_results
from report.json_report import save_json_report


def main():
    parser = argparse.ArgumentParser(description="Advanced Network Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=100)

    args = parser.parse_args()

    print(f"\nScanning target: {args.target}\n")

    scan_id, results, duration = run_scan(
        args.target,
        start_port=args.start,
        end_port=args.end,
        threads=args.threads
    )

    print_results(results, duration)
    save_json_report(scan_id, args.target, results, duration)


if __name__ == "__main__":
    main()
