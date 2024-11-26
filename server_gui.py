import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import os
import signal

class ServerControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contrôle du Serveur")
        self.geometry("300x200")

        self.server_process = None

        self.create_widgets()

    def create_widgets(self):
        self.status_label = ttk.Label(self, text="Serveur'nay", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5, padx=5)

        start_button = ttk.Button(self, text="Démarrer le Serveur", command=self.start_server)
        start_button.pack(pady=10)

        stop_button = ttk.Button(self, text="Arrêter le Serveur", command=self.stop_server)
        stop_button.pack(pady=10)

    def start_server(self):
        if self.server_process is None:
            self.server_process = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            threading.Thread(target=self.update_status, daemon=True).start()
            messagebox.showinfo("Info", "Le serveur a démarré avec succès !")
        else:
            messagebox.showinfo("Info", "Le serveur est déjà en cours d'exécution")

    def stop_server(self):
        if self.server_process is not None:
            os.kill(self.server_process.pid, signal.SIGTERM)
            self.server_process = None
            self.status_label.config(text="Serveur arrêté")
            messagebox.showinfo("Info", "Le serveur a été arrêté avec succès !")
        else:
            messagebox.showinfo("Info", "Le serveur n'est pas en cours d'exécution")

    def update_status(self):
        if self.server_process:
            for line in iter(self.server_process.stdout.readline, b''):
                if b'Running on' in line:
                    self.status_label.config(text="Serveur en cours d'exécution")
                if b'Terminating' in line:
                    self.status_label.config(text="Serveur arrêté")
                    break

if __name__ == "__main__":
    app = ServerControlApp()
    app.mainloop()
