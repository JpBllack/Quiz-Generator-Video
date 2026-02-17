import os
import requests
from dotenv import load_dotenv

# Carrega as chaves
load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # ID da voz "Adam" (Narrador Americano Padrão)

def gerar_audio(texto, nome_arquivo):
    """
    Envia o texto para a ElevenLabs e salva o MP3.
    """
    if not ELEVEN_API_KEY:
        print("❌ Erro: Chave ELEVEN_API_KEY não encontrada no .env")
        return False

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }

    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2", # Modelo que fala português bem
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print(f"🎤 Gerando áudio: '{texto[:30]}...'")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Garante que a pasta existe
            caminho_completo = os.path.join("assets", "audio", nome_arquivo)
            os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)
            
            with open(caminho_completo, "wb") as f:
                f.write(response.content)
            print(f"💾 Salvo em: {caminho_completo}")
            return caminho_completo
        else:
            print(f"❌ Erro na ElevenLabs ({response.status_code}): {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def processar_vozes_do_quiz(quiz_data):
    """
    Itera sobre as perguntas e gera um áudio para cada uma.
    Retorna a lista atualizada com o caminho dos áudios.
    """
    print("\n--- 🔊 Iniciando Geração de Voz ---")
    
    for i, item in enumerate(quiz_data):
        # Texto que será falado no vídeo
        # Ex: "Pergunta 1: Qual a capital do Brasil?"
        texto_narracao = f"Pergunta {i+1}: {item['pergunta']}"
        
        nome_arquivo = f"pergunta_{i+1}.mp3"
        
        # Gera o áudio
        caminho = gerar_audio(texto_narracao, nome_arquivo)
        
        # Salva o caminho no dicionário para usar no vídeo depois
        if caminho:
            item["audio_path"] = caminho
        else:
            print(f"⚠️ Pulei o áudio da pergunta {i+1} por erro.")

    return quiz_data