from threading import Thread
import tkinter as tk
from tkinter import messagebox

from downloader import baixar_audio_mp3


def criar_interface():
    interface = tk.Tk()
    interface.title("Conversor de video para MP3")

    # Label e campo de entrada para o URL
    tk.Label(interface, text="URL do YouTube:").pack(pady=5)
    url_entry = tk.Entry(interface, width=50)
    url_entry.pack(pady=5, padx=10)

    # Label de status
    status_label = tk.Label(interface, text="Pronto para download.")
    status_label.pack(pady=10)

    # Botão de download
    download_button = tk.Button(
        interface,
        text="Baixar MP3",
        command=lambda: iniciar_download_thread(interface, url_entry, status_label)
    )
    download_button.pack(pady=10)

    interface.mainloop()

def iniciar_download_thread(interface_principal, url_entry, status_label):
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira um URL.")
        return

    def update_status(message, is_error=False):
        """Função para atualizar a label de status na thread principal da interface."""
        status_label.config(text=message, fg='red' if is_error else 'black')
        interface_principal.update()

    # Criar e iniciar uma nova thread para o download
    download_thread = Thread(target=baixar_audio_mp3, args=(url, update_status))
    download_thread.start()
