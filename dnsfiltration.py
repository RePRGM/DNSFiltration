import subprocess
import ipaddress
import argparse
import random

def run_nslookup(ip):
    try:
        result = subprocess.run(['nslookup', str(ip)], capture_output=True, text=True, timeout=3)
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"{ip} - Timeout"
    except Exception as e:
        return f"{ip} - Error: {e}"

def scan_ip_range(start_ip, end_ip, keyword, output_file=None):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    if start > end:
        print("Start IP must be less than or equal to End IP.")
        return

    matches = []

    # Generate and shuffle IPs
    ip_list = [ipaddress.IPv4Address(ip) for ip in range(int(start), int(end) + 1)]
    random.shuffle(ip_list)

    for ip_obj in ip_list:
        ip_str = str(ip_obj)
        print(f"\rScanning {ip_str}...", end="", flush=True)
        output = run_nslookup(ip_str)
        if keyword.lower() in output.lower():
            print(f"\r✔ Match found: {ip_str}{' ' * 20}")
            matches.append(f"{ip_str}\n{output}\n")

    print("\rScanning complete.              ")

    if output_file:
        with open(output_file, "w") as f:
            f.writelines(matches)
        print(f"\nSaved {len(matches)} matches to {output_file}")
    else:
        print(f"\nFound {len(matches)} matching results:")
        for match in matches:
            print(match)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run nslookup on an IP range and filter results by keyword.")
    parser.add_argument("-s", "--start", required=True, help="Start IP address (e.g., 192.168.1.1)")
    parser.add_argument("-e", "--end", required=True, help="End IP address (e.g., 192.168.1.254)")
    parser.add_argument("-k", "--keyword", required=True, help="Keyword to search for in nslookup results")
    parser.add_argument("-o", "--output", help="Optional: Output file to save results")

    args = parser.parse_args()
    scan_ip_range(args.start, args.end, args.keyword, args.output)
