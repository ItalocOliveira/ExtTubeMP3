from threading import Thread
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from downloader import baixar_audio_mp3


def criar_interface():
    interface = tk.Tk()
    interface.title("Conversor de video para MP3")

    # Configurações da interface
    interface.geometry("600x400")
    padding_y = 10
    largura_entrada = 60

    # Label e campo de entrada para o URL
    tk.Label(interface, text="URL do YouTube:", font=("Arial", 12)).pack(pady=padding_y)
    url_entry = tk.Entry(interface, width=largura_entrada, font=("Arial", 10))
    url_entry.pack(pady=5, padx=20)

    # Seleção do destino dos downloads
    caminho_destino_var = tk.StringVar(interface, value="")

    tk.Label(interface, text="Pasta de Destino:", font=("Arial", 12)).pack(pady=padding_y)

    botao_selecionar_pasta = tk.Button(
        interface,
        text="Selecionar Pasta",
        font=("Arial", 10),
        command=lambda: selecionar_pasta(caminho_destino_var)
    )
    botao_selecionar_pasta.pack(pady=5)

    caminho_entry = tk.Entry(interface, width=largura_entrada, textvariable=caminho_destino_var, font=("Arial", 10))
    caminho_entry.pack(pady=5, padx=20)

    status_label = tk.Label(interface, text="Pronto para download.", font=("Arial", 10))
    status_label.pack(pady=padding_y)

    # Botão de download
    download_button = tk.Button(
        interface,
        text="Baixar MP3",
        font=("Arial", 14, "bold"),
        command=lambda: iniciar_download_thread(interface, url_entry, status_label, caminho_destino_var)
    )
    download_button.pack(pady=padding_y * 2)

    interface.mainloop()

def selecionar_pasta(caminho_destino_var):
    pasta_selecionada = filedialog.askdirectory()

    if pasta_selecionada:
        caminho_destino_var.set(pasta_selecionada)

def iniciar_download_thread(interface_principal, url_entry, status_label, caminho_destino_var):
    url = url_entry.get()

    pasta_destino = caminho_destino_var.get()

    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira um URL.")
        return
    if not pasta_destino:
        messagebox.showwarning("Aviso", "Por favor, selecione uma pasta de destino.")
        return

    def update_status(message, is_error=False):
        """Função para atualizar a label de status na thread principal da interface."""
        status_label.config(text=message, fg='red' if is_error else 'black')
        interface_principal.update()

    # Criar e iniciar uma nova thread para o download
    download_thread = Thread(target=baixar_audio_mp3, args=(url, update_status, pasta_destino))
    download_thread.start()
