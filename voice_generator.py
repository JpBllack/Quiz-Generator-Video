import os
import requests
from dotenv import load_dotenv

# Carrega as chaves
load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Voz do Adam (Narrador)

def gerar_audio(texto, nome_arquivo):
    """
    Gera o áudio APENAS se ele ainda não existir na pasta.
    Economiza créditos da API.
    """
    # Garante que a pasta existe
    caminho_pasta = os.path.join("assets", "audio")
    os.makedirs(caminho_pasta, exist_ok=True)
    
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

    # --- 🛑 AQUI ESTÁ A ECONOMIA DE DINHEIRO ---
    if os.path.exists(caminho_completo):
        print(f"♻️ Áudio já existe (Cache): {nome_arquivo}")
        return caminho_completo
    # -------------------------------------------

    if not ELEVEN_API_KEY:
        print("❌ Erro: Chave ELEVEN_API_KEY não encontrada no .env")
        return None

    print(f"🎤 Gerando NOVO áudio na ElevenLabs: '{texto[:30]}...'")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }

    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(caminho_completo, "wb") as f:
                f.write(response.content)
            print(f"💾 Salvo e baixado: {caminho_completo}")
            return caminho_completo
        else:
            print(f"❌ Erro na ElevenLabs ({response.status_code}): {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return None

def processar_vozes_do_quiz(quiz_data):
    print("\n--- 🔊 Verificando Áudios ---")
    
    for i, item in enumerate(quiz_data):
        texto_narracao = f"Pergunta {i+1}: {item['pergunta']}"
        nome_arquivo = f"pergunta_{i+1}.mp3"
        
        caminho = gerar_audio(texto_narracao, nome_arquivo)
        
        if caminho:
            item["audio_path"] = caminho
        else:
            print(f"⚠️ Pulei o áudio da pergunta {i+1} por erro.")

    return quiz_data