"""
Analisador de vídeo do YouTube
Baixa o áudio, transcreve e manda pro resumo da IA
"""

import os
import sys

# Coloca suas chaves aqui
ANTHROPIC_API_KEY = "COLOQUE_SUA_CHAVE_DA_ANTHROPIC_AQUI"
OPENAI_API_KEY = "COLOQUE_SUA_CHAVE_DA_OPENAI_AQUI"

# Escolhe a IA: "claude" ou "chatgpt"
IA = "claude"

# Modelo do Whisper (base é mais rápido, large é mais preciso)
MODELO_WHISPER = "base"

ARQUIVO_AUDIO = "audio_baixado"


def baixar_audio(url):
    print("\nBaixando o áudio do vídeo...")
    print("Pode demorar um pouco dependendo do tamanho.\n")

    import yt_dlp

    opcoes = {
        "format": "bestaudio/best",
        "outtmpl": ARQUIVO_AUDIO + ".%(ext)s",
        "quiet": False,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get("title", "video_sem_titulo")
    except Exception as e:
        print("Erro ao baixar o áudio:")
        print(e)
        sys.exit(1)

    caminho = ARQUIVO_AUDIO + ".mp3"

    if os.path.exists(caminho):
        print("Áudio baixado com sucesso!")
        print(f"Arquivo: {caminho}")
    else:
        print("Não encontrei o arquivo de áudio. Algo deu errado.")
        sys.exit(1)

    return caminho, titulo


def transcrever_audio(caminho_audio):
    print("\nTranscrevendo o áudio...")
    print("Essa parte demora bastante, principalmente se o vídeo for longo.\n")

    import whisper

    try:
        modelo = whisper.load_model(MODELO_WHISPER)
        resultado = modelo.transcribe(caminho_audio, language="pt")
        texto = resultado["text"]
    except Exception as e:
        print("Erro na transcrição:")
        print(e)
        sys.exit(1)

    print("Transcrição concluída!")
    return texto


def resumir_texto(texto, titulo):
    print("\nMandando o texto pra IA resumir...\n")

    prompt = f"""Resuma o conteúdo do vídeo abaixo de forma clara e objetiva.
Título do vídeo: {titulo}

Transcrição:
{texto}
"""

    try:
        if IA == "claude":
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            mensagem = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            resumo = mensagem.content[0].text

        elif IA == "chatgpt":
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            resumo = resposta.choices[0].message.content

        else:
            print("IA inválida. Use 'claude' ou 'chatgpt'.")
            sys.exit(1)

    except Exception as e:
        print("Erro ao chamar a IA:")
        print(e)
        sys.exit(1)

    return resumo


def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py <url_do_video>")
        sys.exit(1)

    url = sys.argv[1]

    caminho_audio, titulo = baixar_audio(url)
    texto = transcrever_audio(caminho_audio)
    resumo = resumir_texto(texto, titulo)

    print("\n" + "="*50)
    print("RESUMO DO VÍDEO")
    print("="*50)
    print(f"\nTítulo: {titulo}\n")
    print(resumo)
    print("\n" + "="*50)

    # Opcional: apagar o áudio depois
    # os.remove(caminho_audio)


if __name__ == "__main__":
    main()
