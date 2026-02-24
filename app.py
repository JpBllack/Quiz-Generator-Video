import streamlit as st
import os
import json
from voice_generator import processar_vozes_do_quiz
from video_generator import gerar_video_final

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Fábrica Quiz Mania", page_icon="🎬", layout="centered")

def gerar_nome_sequencial(categoria):
    pasta_destino = os.path.join("assets", "videos_prontos")
    os.makedirs(pasta_destino, exist_ok=True)
    arquivos_existentes = [f for f in os.listdir(pasta_destino) if f.startswith(categoria) and f.endswith(".mp4")]
    proximo_numero = len(arquivos_existentes) + 1
    return f"{categoria}_{proximo_numero}.mp4"

# --- INTERFACE ---
st.title("🎬 Fábrica de Vídeos - Quiz Mania")
st.markdown("Cole seu roteiro JSON gerado pela IA e crie seu vídeo automaticamente.")

# 1. Campo para colar o Roteiro
roteiro_padrao = """[
  {
    "pergunta": "Qual é o maior planeta do nosso sistema solar?",
    "opcoes": ["Marte", "Júpiter", "Saturno"],
    "correta": 1
  }
]"""

roteiro_json = st.text_area("Roteiro do Vídeo (JSON)", value=roteiro_padrao, height=250)

# 2. Escolha do Fundo
tema_escolhido = st.selectbox(
    "🖼️ Escolha o TEMA do vídeo de fundo:",
    ["1 - Cristão / Teologia", "2 - Musculação / Fitness", "3 - Música / Instrumentos", "4 - Aleatório (Minecraft)"]
)

# 3. Botão de Gerar
if st.button("🚀 Gerar Vídeo", type="primary"):
    try:
        # Tenta ler o JSON colado
        quiz_data = json.loads(roteiro_json)
        
        # Salva no arquivo quiz.json (só pro sistema de hash de áudio funcionar certinho)
        with open("quiz.json", "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=4)
            
    except json.JSONDecodeError:
        st.error("❌ Ops! O formato JSON está inválido. Verifique se faltam vírgulas ou aspas.")
        st.stop()

    # Mapeando a escolha do fundo
    if "Cristão" in tema_escolhido:
        caminho_fundo = os.path.join("assets", "background_cristao.mp4")
        categoria = "cristao"
    elif "Musculação" in tema_escolhido:
        caminho_fundo = os.path.join("assets", "background_musculacao.mp4")
        categoria = "musculacao"
    elif "Música" in tema_escolhido:
        caminho_fundo = os.path.join("assets", "background_musica.mp4")
        categoria = "musica"
    else:
        caminho_fundo = os.path.join("assets", "background_minecraft.mp4")
        categoria = "aleatorio"

    nome_video = gerar_nome_sequencial(categoria)
    caminho_final = os.path.join("assets", "videos_prontos", nome_video)

    # --- INÍCIO DA GERAÇÃO COM FEEDBACK VISUAL ---
    with st.status("🛠️ Fabricando seu vídeo...", expanded=True) as status:
        st.write("🎤 Gerando áudios na ElevenLabs...")
        try:
            quiz_com_audio = processar_vozes_do_quiz(quiz_data)
        except Exception as e:
            st.error(f"Erro no áudio: {e}")
            st.stop()
            
        st.write(f"🎬 Renderizando vídeo de fundo: {categoria}...")
        gerar_video_final(quiz_com_audio, nome_video, caminho_fundo)
        
        status.update(label="✅ Vídeo finalizado com sucesso!", state="complete", expanded=False)

    # Exibe o player de vídeo na tela
    st.success(f"Vídeo salvo em: {caminho_final}")
    st.video(caminho_final)


    