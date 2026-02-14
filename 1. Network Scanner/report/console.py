def print_results(results, duration):
    print("\nScan complete")
    print(f"Scan duration: {duration} seconds")
    print("Open ports:\n")

    for port, data in results.items():
        print(f"{port}: {data['service']} -> {data['banner']}")
