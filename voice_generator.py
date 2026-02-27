import os
import glob
import json
import hashlib
import asyncio
import edge_tts

# Voz padrão da Microsoft (Brasileira, Masculina). 
VOZ_PADRAO = "pt-BR-AntonioNeural" 

async def gerar_audio_async(texto, caminho_completo):
    # rate="+10%" deixa a voz mais dinâmica para reter atenção
    communicate = edge_tts.Communicate(texto, VOZ_PADRAO, rate="+10%")
    await communicate.save(caminho_completo)

def gerar_audio(texto, nome_arquivo):
    caminho_pasta = os.path.join("assets", "audio")
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

    if os.path.exists(caminho_completo):
        print(f"♻️ Áudio já em cache: {nome_arquivo}")
        return caminho_completo

    print(f"🎤 Baixando NOVO áudio (Edge TTS): '{texto[:30]}...'")
    
    try:
        asyncio.run(gerar_audio_async(texto, caminho_completo))
        print(f"💾 Salvo em: {caminho_completo}")
        return caminho_completo
    except Exception as e:
        print(f"❌ Erro de conexão com TTS: {e}")
        return None

def processar_vozes_do_quiz(quiz_data):
    print("\n--- 🔊 Iniciando Geração de Voz (Microsoft Edge) ---")
    
    caminho_pasta = os.path.join("assets", "audio")
    os.makedirs(caminho_pasta, exist_ok=True)
    arquivo_hash = os.path.join(caminho_pasta, "quiz_hash.txt")

    # Verifica se o roteiro mudou para apagar os áudios antigos
    conteudo_json = json.dumps(quiz_data, sort_keys=True, ensure_ascii=False)
    hash_atual = hashlib.md5(conteudo_json.encode('utf-8')).hexdigest()

    hash_salvo = ""
    if os.path.exists(arquivo_hash):
        with open(arquivo_hash, "r") as f:
            hash_salvo = f.read().strip()

    if hash_atual != hash_salvo:
        print("🚨 NOVO ROTEIRO DETECTADO! Limpando áudios antigos...")
        arquivos_antigos = glob.glob(os.path.join(caminho_pasta, "pergunta_*.mp3"))
        for arq in arquivos_antigos:
            try:
                os.remove(arq)
            except Exception as e:
                pass
                
        with open(arquivo_hash, "w") as f:
            f.write(hash_atual)
    else:
        print("✅ O roteiro é o mesmo. Validando cache existente...")

    # Gera vozes APENAS das perguntas (como era na versão original)
    for i, item in enumerate(quiz_data):
        texto_narracao = f"{item['pergunta']}"
        nome_arquivo = f"pergunta_{i+1}.mp3"
        
        caminho = gerar_audio(texto_narracao, nome_arquivo)
        
        if caminho:
            item["audio_path"] = caminho
        else:
            print(f"⚠️ Pulei o áudio da pergunta {i+1} por erro.")

    # --- GERA O ÁUDIO DO ENCERRAMENTO ---
    print("\n🎤 Verificando áudio de encerramento...")
    texto_encerramento = "Quantas você acertou? Deixe nos comentários! Curta e siga para mais."
    gerar_audio(texto_encerramento, "encerramento.mp3")

    return quiz_data