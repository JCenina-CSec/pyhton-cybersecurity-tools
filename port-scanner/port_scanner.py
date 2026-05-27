"""
File Name: Port_Scanner.py
Author: John Cenina
Purpose: Scan a specified range of TCP ports on a target IP or hostname.
Date Started: 12/11/2025
Date Completed: 19/11/2025

LEGAL NOTICE:
Only scan hosts you own or have explicit permission to scan.
Unauthorized port scanning may be illegal and unethical.
"""

import os
import socket
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------
# Logging configuration with header
# ----------------------------
log_file = "port_scan_log.txt"

# Write header if file does not exist
if not os.path.exists(log_file):
    with open(log_file, "a") as f:
        f.write("Timestamp - Port - Status\n")

logging.basicConfig(
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)


def scan_port(target_host, port):
    """
    Attempts to connect to a specific port on the target host.
    Returns the port number if open, None otherwise.
    Logs errors if connection fails unexpectedly.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # 0.5 second wait

        result = s.connect_ex((target_host, port))

        if result == 0:
            logging.info(f"Port {port} OPEN")
            return port  # Return port number if open
        return None

    except socket.error as error:
        logging.error(f"Error scanning port {port}: {error}")
        return None

    finally:
        s.close()


def validate_ports(start_port, end_port):
    """
    Validates that both ports are within 0–65535 and start <= end.
    """
    if not (0 <= start_port <= 65535 and 0 <= end_port <= 65535):
        print("Error: Port numbers must be between 0 and 65535.")
        return False

    if start_port > end_port:
        print("Error: Start port must be less than or equal to end port.")
        return False

    return True


def main():
    """
    Main program: collects input, validates it, scans ports using ThreadPoolExecutor,
    prints open ports, and logs results.
    """

    target = input("\nEnter the target IP address or hostname: ")

    # Validate numeric port input
    try:
        start_port = int(input("Enter the starting port number: "))
        end_port = int(input("Enter the ending port number: "))
    except ValueError:
        print("Error: Port numbers must be integers.")
        return

    if not validate_ports(start_port, end_port):
        return

    print(f"\nScanning ports on {target} from {start_port} to {end_port}...\n")

    open_ports = []

    # Use ThreadPoolExecutor for safe parallel scanning
    with ThreadPoolExecutor(max_workers=50) as executor:  # Limit concurrent threads
        future_to_port = {executor.submit(scan_port, target, port): port for port in range(start_port, end_port + 1)}

        for future in as_completed(future_to_port):
            port = future.result()
            if port:
                print(f"Port {port} is OPEN")
                open_ports.append(port)

    print("\nScan complete. Results saved to port_scan_log.txt")
    print(f"Total open ports: {len(open_ports)}")


if __name__ == "__main__":
    print("\n===== Port Scanner =====\n")

    while True:
        main()
        again = input("\nDo you want to run another scan? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting program, until next time.")
            break