import socket
import concurrent.futures
import sys
import subprocess
import warnings
import os

# Suppress specific deprecation warning from Paramiko
warnings.filterwarnings("ignore", category=DeprecationWarning, message="TripleDES has been moved")

# Function to scan a single port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return port, True
        else:
            return port, False
    except Exception as e:
        return port, False, str(e)
    finally:
        sock.close()

# Function to get a list of open ports
def scan_ports(ip, start_port, end_port):
    open_ports = []
    errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result = future.result()
                if len(result) == 2:
                    port, is_open = result
                    if is_open:
                        open_ports.append(port)
                else:
                    port, is_open, error = result
                    if is_open:
                        open_ports.append(port)
                    else:
                        errors.append(f"Port {port}: {error}")
            except Exception as exc:
                errors.append(f"Port {port} generated an exception: {exc}")

    return open_ports, errors

# Function to get local IP addresses
def get_local_ips():
    local_ips = []
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    local_ips.append(local_ip)

    try:
        # Using ip command instead of hostname -I for better compatibility
        output = subprocess.check_output(['ip', 'addr', 'show']).decode().split()
        ips = [ip for ip in output if ip.startswith("inet") and not ip.startswith("inet6")]
        local_ips.extend([ip.split('/')[0].split('inet')[1].strip() for ip in ips])
    except Exception as e:
        print(f"Error retrieving local IP addresses: {e}")

    # Remove any empty or duplicate entries
    local_ips = list(filter(None, local_ips))
    local_ips = list(set(local_ips))

    return local_ips

# Function to check required packages
def check_requirements():
    required_packages = ["requests", "beautifulsoup4", "scapy", "paramiko", "pynput", "mitmproxy"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to check if running in a virtual environment
def check_venv():
    if sys.prefix == sys.base_prefix:
        return False
    return True

# Main function to interact with the user and perform the port scan
def main():
    print("Welcome To Port Scanner")

    if not check_venv():
        print("You are not running inside a virtual environment.")
        while True:
            enter_venv = input("Would you like to activate a virtual environment? (yes/no): ").strip().lower()
            if enter_venv == 'yes':
                venv_path = input("Enter the path to your virtual environment: ").strip()
                if os.path.exists(os.path.join(venv_path, 'bin', 'activate')):
                    activate_script = os.path.join(venv_path, 'bin', 'activate')
                    exec(open(activate_script).read(), {'__file__': activate_script})
                    break
                else:
                    print("The specified path does not contain a valid virtual environment. Please try again.")
            elif enter_venv == 'no':
                print("Continuing without activating a virtual environment.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    check_requirements()

    local_ips = get_local_ips()
    if local_ips:
        print("\nAvailable IP addresses on the local network:")
        for idx, ip in enumerate(local_ips, 1):
            print(f"{idx}. {ip}")

        ip_choice = input("\nSelect an IP address by number or enter a custom IP: ")
        if ip_choice.isdigit() and 1 <= int(ip_choice) <= len(local_ips):
            ip = local_ips[int(ip_choice) - 1]
        else:
            ip = ip_choice
    else:
        ip = input("Enter a custom IP address: ")

    while True:
        try:
            start_port = int(input("Enter the start port: "))
            end_port = int(input("Enter the end port: "))
            if start_port < 0 or end_port < 0 or start_port > end_port:
                raise ValueError
            break
        except ValueError:
            print("Please enter valid port numbers (start port <= end port and both non-negative).")

    print(f"\nScanning {ip} from port {start_port} to {end_port}...\n")

    open_ports, errors = scan_ports(ip, start_port, end_port)

    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(f"Port {port} is open")
    else:
        print("No open ports found.")

    if errors:
        print("\nErrors encountered during scanning:")
        for error in errors:
            print(error)

    print("\nScan complete.")

    while True:
        next_action = input("\nDo you want to scan another IP or port range? (yes/no): ").strip().lower()
        if next_action == 'yes':
            main()
        elif next_action == 'no':
            print("Exiting program.")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan aborted by user.")
        sys.exit(0)

