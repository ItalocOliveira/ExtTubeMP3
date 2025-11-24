import platform
import yt_dlp
import os

# Prompt: yt-dlp -i --extract-audio --audio-format mp3 --audio-quality 0 --yes-playlist [URL] -o "%(title)s.%(ext)s"

def baixar_audio_mp3(url, status_callback):

    # Configuração para o caminho do ffmpeg
    ffmpeg_executavel = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
    ffmpeg_dir = os.path.join(os.getcwd(), 'docs/ffmpeg/bin')

    ffmpeg_path_completo = os.path.join(ffmpeg_dir, ffmpeg_executavel)
    if not os.path.exists(ffmpeg_path_completo):
        print(f"ERRO: Não foi possível encontrar o FFmpeg em: {ffmpeg_dir}")
        print("Certifique-se de que a pasta 'ffmpeg' (contendo ffmpeg.exe e ffprobe.exe) está na raiz do seu projeto.")
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
        # --no-overwrites: Nega overwrite de arquivos (Ativo como padrão)
        'overwrites': False,
        # -o "%(title)s.%(ext)s": Nomear o arquivo com o título e a extensão correta.
        'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
        # Caminho para a utilização do ffmpeg
        'ffmpeg_location': ffmpeg_dir,

        # Progress hook para enviar status de volta
        'progress_hooks': [lambda d: status_callback(d['status'])],
    }

    status_callback(f"Iniciando download. Usando FFmpeg de: {ffmpeg_dir}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_callback("Download e conversão concluídos!", is_error=False)
    except Exception as error:
        status_callback(f"ERRO CRÍTICO: {error}", is_error=True)


