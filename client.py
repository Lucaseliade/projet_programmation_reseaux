import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client")
        self.geometry("700x500")
        
        self.server_url = "http://127.0.0.1:5000"
        self.all_server_files = []  # Liste complète des fichiers sur le serveur
        self.downloaded_files = []  # Liste des fichiers téléchargés localement

        self.create_widgets()

    def create_widgets(self):
        # Section pour la recherche
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Rechercher :").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_files)

        # Section pour les fichiers sur le serveur
        tk.Label(self, text="Fichiers sur le serveur :").pack(pady=5)

        # Frame pour la liste des fichiers serveur avec barre de défilement
        server_frame = tk.Frame(self)
        server_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.server_file_list = tk.Listbox(server_frame, height=8)
        self.server_file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        server_scrollbar = tk.Scrollbar(server_frame, orient=tk.VERTICAL, command=self.server_file_list.yview)
        server_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.server_file_list.config(yscrollcommand=server_scrollbar.set)

        # Section pour les fichiers téléchargés
        tk.Label(self, text="Fichiers téléchargés :").pack(pady=5)

        # Frame pour la liste des fichiers téléchargés avec barre de défilement
        downloaded_frame = tk.Frame(self)
        downloaded_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.downloaded_file_list = tk.Listbox(downloaded_frame, height=8)
        self.downloaded_file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        downloaded_scrollbar = tk.Scrollbar(downloaded_frame, orient=tk.VERTICAL, command=self.downloaded_file_list.yview)
        downloaded_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.downloaded_file_list.config(yscrollcommand=downloaded_scrollbar.set)

        # Frame pour les boutons, toujours en bas
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Téléverser un fichier", command=self.upload_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Télécharger un fichier", command=self.download_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualiser la liste", command=self.refresh_file_list).pack(side=tk.LEFT, padx=5)

        self.refresh_file_list()  # Charger initialement les fichiers disponibles sur le serveur

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                response = requests.post(f"{self.server_url}/upload", files={"file": f})
                if response.status_code == 200:
                    messagebox.showinfo("Succès", "Fichier téléversé avec succès !")
                    self.refresh_file_list()
                else:
                    messagebox.showerror("Erreur", "Échec du téléversement du fichier")

    def download_file(self):
        selected_file = self.server_file_list.get(tk.ACTIVE)
        if selected_file:
            response = requests.get(f"{self.server_url}/files/{selected_file}")
            if response.status_code == 200:
                save_path = filedialog.asksaveasfilename(initialfile=selected_file)
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    messagebox.showinfo("Succès", "Fichier téléchargé avec succès !")
                    # Ajouter le fichier téléchargé à la liste des fichiers téléchargés
                    self.downloaded_files.append(selected_file)
                    self.update_downloaded_file_list()
            else:
                messagebox.showerror("Erreur", "Échec du téléchargement du fichier")

    def refresh_file_list(self):
        """Récupère la liste des fichiers sur le serveur et met à jour l'affichage."""
        response = requests.get(f"{self.server_url}/files")
        if response.status_code == 200:
            self.all_server_files = response.json()
            self.update_server_file_list(self.all_server_files)
        else:
            messagebox.showerror("Erreur", "Échec de la récupération de la liste des fichiers sur le serveur")

    def update_server_file_list(self, files):
        """Met à jour la liste affichée des fichiers serveur."""
        self.server_file_list.delete(0, tk.END)
        for file in files:
            self.server_file_list.insert(tk.END, file)

    def update_downloaded_file_list(self):
        """Met à jour la liste affichée des fichiers téléchargés."""
        self.downloaded_file_list.delete(0, tk.END)
        for file in self.downloaded_files:
            self.downloaded_file_list.insert(tk.END, file)

    def filter_files(self, event=None):
        """Filtre les fichiers affichés en fonction de la recherche."""
        query = self.search_entry.get().lower()
        filtered_files = [file for file in self.all_server_files if query in file.lower()]
        self.update_server_file_list(filtered_files)

if __name__ == "__main__":
    app = FileClientApp()
    app.mainloop()
