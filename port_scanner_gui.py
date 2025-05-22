import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def scan_port(host, port, results, progress_callback):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            results.append(port)
        sock.close()
    except:
        pass
    progress_callback()

def start_scan():
    host = entry_host.get().strip()

    try:
        resolved_ip = socket.gethostbyname(host)
    except socket.gaierror:
        messagebox.showerror("Invalid Host", f"Could not resolve '{host}'. Check your spelling or internet connection.")
        return

    try:
        start = int(entry_start.get())
        end = int(entry_end.get())
    except ValueError:
        messagebox.showerror("Input Error", "Port numbers must be integers.")
        return

    if start < 1 or end > 65535 or start > end:
        messagebox.showerror("Input Error", "Invalid port range.")
        return

    output_box.delete("1.0", tk.END)
    progress["value"] = 0
    scan_button.config(state="disabled")
    total_ports = end - start + 1
    progress["maximum"] = total_ports
    results = []

    def update_progress():
        progress["value"] += 1
        root.update_idletasks()

    def run_scan():
        for port in range(start, end + 1):
            scan_port(host, port, results, update_progress)
        output_box.insert(tk.END, f"Scan complete for {host}\n")
        if results:
            output_box.insert(tk.END, f"Open ports: {', '.join(map(str, results))}\n")
        else:
            output_box.insert(tk.END, "No open ports found.\n")
        scan_button.config(state="normal")

    threading.Thread(target=run_scan).start()

# GUI Setup
root = tk.Tk()
root.title("Port Scanner")
root.geometry("400x400")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Target Host/IP:").grid(row=0, column=0, sticky="e")
entry_host = tk.Entry(frame)
entry_host.grid(row=0, column=1)

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

output_box = scrolledtext.ScrolledText(root, height=10, width=45)
output_box.pack(pady=10)

root.mainloop()
