import os
import glob
import json
import hashlib
import requests
from dotenv import load_dotenv

# Carrega as chaves
load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # ID da voz "Adam"

def gerar_audio(texto, nome_arquivo):
    caminho_pasta = os.path.join("assets", "audio")
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

    if os.path.exists(caminho_completo):
        print(f"♻️ Áudio já em cache: {nome_arquivo}")
        return caminho_completo

    if not ELEVEN_API_KEY:
        print("❌ Erro: Chave ELEVEN_API_KEY não encontrada no .env")
        return None

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

    print(f"🎤 Baixando NOVO áudio da ElevenLabs: '{texto[:30]}...'")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
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
    print("\n--- 🔊 Iniciando Geração de Voz ---")
    
    caminho_pasta = os.path.join("assets", "audio")
    os.makedirs(caminho_pasta, exist_ok=True)
    arquivo_hash = os.path.join(caminho_pasta, "quiz_hash.txt")

    conteudo_json = json.dumps(quiz_data, sort_keys=True, ensure_ascii=False)
    hash_atual = hashlib.md5(conteudo_json.encode('utf-8')).hexdigest()

    hash_salvo = ""
    if os.path.exists(arquivo_hash):
        with open(arquivo_hash, "r") as f:
            hash_salvo = f.read().strip()

    if hash_atual != hash_salvo:
        print("🚨 NOVO ROTEIRO DETECTADO! Limpando áudios antigos das perguntas...")
        arquivos_antigos = glob.glob(os.path.join(caminho_pasta, "pergunta_*.mp3"))
        for arq in arquivos_antigos:
            try:
                os.remove(arq)
            except Exception as e:
                print(f"⚠️ Não consegui apagar {arq}: {e}")
                
        with open(arquivo_hash, "w") as f:
            f.write(hash_atual)
    else:
        print("✅ O roteiro é o mesmo. Validando cache existente...")

    # Gera vozes das perguntas
    for i, item in enumerate(quiz_data):
        texto_narracao = f"Pergunta {i+1}: {item['pergunta']}"
        nome_arquivo = f"pergunta_{i+1}.mp3"
        
        caminho = gerar_audio(texto_narracao, nome_arquivo)
        
        if caminho:
            item["audio_path"] = caminho
        else:
            print(f"⚠️ Pulei o áudio da pergunta {i+1} por erro.")

    # --- NOVO: GERA O ÁUDIO DO ENCERRAMENTO ---
    print("\n🎤 Verificando áudio de encerramento...")
    texto_encerramento = "Quantas você acertou? Deixe nos comentários! Curta e siga para mais."
    gerar_audio(texto_encerramento, "encerramento.mp3")

    return quiz_data