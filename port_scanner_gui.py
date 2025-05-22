import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def scan_port(host, port, results, update_progress):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                results.append(port)
    except Exception:
        pass
    update_progress()

def start_scan():
    host = entry_host.get().strip()

    try:
    resolved_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        messagebox.showerror(
            "Invalid Host", 
            f"Could not resolve '{host}'.\nError: {e}\n\nTry using a correct domain name or IP address."
        )
        return


    try:
        start_port = int(entry_start.get())
        end_port = int(entry_end.get())
        if not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535) or start_port > end_port:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid port range (1–65535).")
        return

    output_box.delete("1.0", tk.END)
    progress["value"] = 0
    progress["maximum"] = end_port - start_port + 1
    scan_button.config(state="disabled")

    results = []

    def update_progress():
        progress["value"] += 1
        root.update_idletasks()

    def run_scan():
        for port in range(start_port, end_port + 1):
            scan_port(resolved_ip, port, results, update_progress)

        output_box.insert(tk.END, f"Scan complete for {host} ({resolved_ip})\n")
        if results:
            output_box.insert(tk.END, f"Open ports: {', '.join(map(str, results))}\n")
        else:
            output_box.insert(tk.END, "No open ports found.\n")

        scan_button.config(state="normal")

    threading.Thread(target=run_scan, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Port Scanner")
root.geometry("420x400")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Target Host/IP:").grid(row=0, column=0, sticky="e")
entry_host = tk.Entry(frame)
entry_host.grid(row=0, column=1)
entry_host.insert(0, "127.0.0.1")

tk.Label(frame, text="Start Port:").grid(row=1, column=0, sticky="e")
entry_start = tk.Entry(frame)
entry_start.grid(row=1, column=1)
entry_start.insert(0, "1")

tk.Label(frame, text="End Port:").grid(row=2, column=0, sticky="e")
entry_end = tk.Entry(frame)
entry_end.grid(row=2, column=1)
entry_end.insert(0, "1024")

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, height=10, width=50)
output_box.pack(pady=10)

root.mainloop()
