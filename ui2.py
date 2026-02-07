from modules.network_scanner import NetworkScanner
from modules.password_attack_simulator import NetworkScanner, WiFiConnector
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading


class WiFiAuditUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Security Auditor")
        self.root.geometry("700x550")

        self.networks = []
        self.selected_ssid = None

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="WiFi Security Auditor", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.root, text="Scan Networks", command=self.scan_networks).pack()

        self.network_list = tk.Listbox(self.root, height=8, width=60)
        self.network_list.pack(pady=10)

        tk.Label(self.root, text="Passwords (one per line):").pack()
        self.password_box = scrolledtext.ScrolledText(self.root, height=8)
        self.password_box.pack(fill=tk.BOTH, padx=10, pady=5)

        self.legal_var = tk.IntVar()
        tk.Checkbutton(
            self.root,
            text="I own this network or have explicit permission",
            variable=self.legal_var
        ).pack(pady=5)

        tk.Button(self.root, text="Start Test", command=self.start_test).pack(pady=10)

        self.output = scrolledtext.ScrolledText(self.root, height=10, state="disabled")
        self.output.pack(fill=tk.BOTH, padx=10)

    def log(self, text):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def scan_networks(self):
        self.network_list.delete(0, tk.END)
        self.log("[*] Scanning networks...")

        try:
            scanner = NetworkScanner()
            self.networks = scanner.scan()
        except Exception as e:
            messagebox.showerror("Scan Error", str(e))
            return

        for net in self.networks:
            ssid = net.get("ssid", "Unknown")
            self.network_list.insert(tk.END, ssid)

        self.log(f"[+] Found {len(self.networks)} networks")

    def start_test(self):
        selection = self.network_list.curselection()
        if not selection:
            messagebox.showwarning("Missing Selection", "Select a network")
            return

        if not self.legal_var.get():
            messagebox.showwarning("Legal Notice", "You must confirm ownership/permission")
            return

        passwords = [
            p.strip() for p in self.password_box.get("1.0", tk.END).splitlines() if p.strip()
        ]

        if not passwords:
            messagebox.showwarning("No Passwords", "Enter at least one password")
            return

        self.selected_ssid = self.network_list.get(selection[0])
        self.log(f"[*] Target: {self.selected_ssid}")
        self.log(f"[*] Passwords loaded: {len(passwords)}")

        thread = threading.Thread(
            target=self.run_test,
            args=(passwords,),
            daemon=True
        )
        thread.start()

    def run_test(self, passwords):
        connector = WiFiConnector(self.selected_ssid)

        result = connector.test_passwords(passwords)

        if result["success"]:
            self.log(f"[+] SUCCESS: {result['password']}")
        else:
            self.log("[-] No valid password found")


if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiAuditUI(root)
    root.mainloop()
