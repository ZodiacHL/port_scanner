import socket

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Half-second timeout
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0  # 0 means the port is open
    except Exception as e:
        return False

def scan_ports(target, start_port=1, end_port=1024):
    print(f"Scanning {target} from port {start_port} to {end_port}...\n")
    open_ports = []
    for port in range(start_port, end_port + 1):
        if scan_port(target, port):
            print(f"Port {port} is OPEN")
            open_ports.append(port)
    if not open_ports:
        print("No open ports found in the specified range.")
    else:
        print(f"\nOpen ports: {open_ports}")

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    start = input("Enter start port (default 1): ")
    end = input("Enter end port (default 1024): ")

    start_port = int(start) if start.isdigit() else 1
    end_port = int(end) if end.isdigit() else 1024

    scan_ports(target, start_port, end_port)

    input("\nPress Enter to exit...")
