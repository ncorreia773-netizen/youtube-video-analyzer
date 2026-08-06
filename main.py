"""
analisador de video do youtube
esse script baixa o audio de um video
depois transcreve o audio
e no final manda o texto pra uma ia resumir
"""

import os
import sys

# aqui eu coloco as chaves das apis
# tem que trocar pelas suas chaves de verdade
ANTHROPIC_API_KEY = "COLOQUE_SUA_CHAVE_DA_ANTHROPIC_AQUI"
OPENAI_API_KEY = "COLOQUE_SUA_CHAVE_DA_OPENAI_AQUI"

# aqui eu escolho qual ia eu quero usar
# pode ser "claude" ou "chatgpt"
IA_ESCOLHIDA = "claude"

# modelo do whisper
# quanto maior o modelo mais demora
MODELO_WHISPER = "base"

# nome do arquivo de audio que vai ser baixado
NOME_DO_ARQUIVO = "audio_baixado"

def baixar_audio_do_video(url_do_video):
    print("")
    print("agora vou baixar o audio do video")
    print("isso pode demorar um pouco dependendo do tamanho")
    print("")

    # importo o yt_dlp aqui dentro
    import yt_dlp

    # monto as opcoes pro download
    opcoes_do_download = {}
    opcoes_do_download["format"] = "bestaudio/best"
    opcoes_do_download["outtmpl"] = NOME_DO_ARQUIVO + ".%(ext)s"
    opcoes_do_download["quiet"] = False
    opcoes_do_download["noplaylist"] = True

    # essa parte e pro ffmpeg converter pra mp3
    post_processor = {}
    post_processor["key"] = "FFmpegExtractAudio"
    post_processor["preferredcodec"] = "mp3"
    post_processor["preferredquality"] = "192"

    lista_de_post = []
    lista_de_post.append(post_processor)
    opcoes_do_download["postprocessors"] = lista_de_post

    try:
        # aqui eu baixo o video
        ydl = yt_dlp.YoutubeDL(opcoes_do_download)
        informacoes = ydl.extract_info(url_do_video, download=True)
        titulo_do_video = informacoes.get("title", "video_sem_titulo")
        ydl.close()
    except Exception as erro_que_deu:
        print("deu erro quando tentei baixar o audio")
        print("o erro foi esse:")
        print(erro_que_deu)
        print("vou sair do programa")
        sys.exit(1)

    # agora eu verifico se o arquivo realmente existe
    caminho_do_audio = NOME_DO_ARQUIVO + ".mp3"
    arquivo_existe = os.path.exists(caminho_do_audio)

    if arquivo_existe == True:
        print("o audio foi baixado com sucesso")
        print("o arquivo esta em:")
        print(caminho_do_audio)
    else:
        print("nao encontrei o arquivo de audio")
        print("algo deu errado no download")
        sys.exit(1)

    return caminho_do_audio, titulo_do_video

def transcrever_o_audio(caminho_do_audio):
    print("")
    print("agora vou transcrever o audio pro texto")
    print("essa parte demora bastante")
    print("principalmente se o video for longo")
    print("")

    # importo o whisper 
