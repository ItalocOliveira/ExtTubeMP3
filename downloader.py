import platform
import yt_dlp
import os
import re

# Prompt inicial: yt-dlp -i --extract-audio --audio-format mp3 --audio-quality 0 --yes-playlist [URL] -o "%(title)s.%(ext)s"

ANSI_ESCAPE_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clean_ansi(text):
    return ANSI_ESCAPE_REGEX.sub('', text)

def progress_hook_callback(d, status_callback):
    if d['status'] == 'downloading':
        # Remove a lógica de extração numérica de porcentagem, pois só usaremos a string formatada
        speed_str = 'N/A'

        # Tenta obter a velocidade de download
        if d.get('_speed_str'):
            speed_str = d['_speed_str']

        # Constrói a mensagem de progresso com porcentagem e velocidade (apenas string)
        raw_message = f"Baixando: {d.get('_percent_str', 'N/A')} a {speed_str}"

        # Limpa os códigos ANSI antes de enviar para o Tkinter
        message = clean_ansi(raw_message)

        # Envia APENAS a mensagem. Remove o argumento 'percent'.
        status_callback(message)

    elif d['status'] == 'finished':
        # Remove o argumento 'percent'
        status_callback("Download concluído, iniciando conversão...")

    elif d['status'] == 'error':
        # A mensagem de erro também pode conter códigos ANSI, então limpamos
        error_message = d.get('error', 'Desconhecido')
        clean_error_message = clean_ansi(error_message)
        # Remove o argumento 'percent'
        status_callback(f"ERRO no download: {clean_error_message}", is_error=True)


def baixar_audio_mp3(url, status_callback, pasta_destino):

    # Configuração para o caminho do ffmpeg
    ffmpeg_executavel = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
    ffmpeg_dir = os.path.join(os.getcwd(), 'docs/ffmpeg/bin')

    ffmpeg_path_completo = os.path.join(ffmpeg_dir, ffmpeg_executavel)
    if not os.path.exists(ffmpeg_path_completo):
        print(f"ERRO: Não foi possível encontrar o FFmpeg em: {ffmpeg_dir}")
        print("Certifique-se de que a pasta 'ffmpeg' (contendo ffmpeg.exe e ffprobe.exe) está na raiz do seu projeto.")
        # Remove o argumento 'percent'
        status_callback(f"ERRO: FFmpeg não encontrado em: {ffmpeg_dir}", is_error=True)
        return

    # Opções do yt-dlp
    ydl_opts = {
        # -i: Ignorar erros em downloads de playlist
        'ignoreerrors': True,
        # --extract-audio: Extrair apenas o áudio
        'extract_audio': True,
        # --audio-format mp3: Converter o áudio para mp3 (erro de ffmpeg, mas funciona)
        'audioformat': 'mp3',
        # --audio-quality 0: Qualidade de áudio de melhor a pior (0 é a melhor, ~256k VBR)
        'audioquality': '0',
        # --yes-playlist: Tratar o URL como uma playlist
        'yes_playlist': True,
        # --no-overwrites: Nega overwrite de arquivos (REMOVIDA para ativar a numeração automática)
        # 'overwrites': False

        # -o "%(title)s.%(ext)s": Nomear o arquivo com o título e a extensão correta.
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),

        # Caminho para a utilização do ffmpeg
        'ffmpeg_location': ffmpeg_dir,

        # Progress hook para enviar status de volta
        'progress_hooks': [lambda d: progress_hook_callback(d, status_callback)],
    }

    # Remove o argumento 'percent'
    status_callback(f"Iniciando download. Destino: {pasta_destino}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_callback("Conversão finalizada com sucesso!", is_error=False)
    except Exception as error:
        status_callback(f"ERRO CRÍTICO: {error}", is_error=True)
