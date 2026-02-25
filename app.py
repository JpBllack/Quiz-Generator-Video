import streamlit as st
import os
import json
import time
from voice_generator import processar_vozes_do_quiz
from video_generator import gerar_video_final

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Fábrica Quiz Mania", page_icon="⚡", layout="centered")

# ==========================================
# 🎨 ESTILO "AURORA GLASS" (Dark & Clean)
# ==========================================
def set_stylized_ui():
    st.markdown(
        """
        <style>
        /* 1. FUNDO ANIMADO (AURORA) */
        .stApp {
            background-color: #000000;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,25%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            background-size: 200% 200%;
            animation: aurora 15s ease infinite;
        }

        @keyframes aurora {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 2. CONTAINER CENTRAL (VIDRO) */
        .block-container {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* 3. TIPOGRAFIA */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            letter-spacing: -1px;
        }
        p, .stMarkdown {
            color: #b0b0b0 !important;
        }

        /* 4. ABAS (Modernas) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(0,0,0,0.2);
            padding: 5px;
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            color: #888;
            border: none;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2d2d2d;
            color: #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        /* 5. INPUTS */
        .stTextArea textarea {
            background-color: #0a0a0a;
            color: white;
            border: 1px solid #333;
            border-radius: 8px;
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #0a0a0a;
            color: white;
            border: 1px solid #333;
            border-radius: 8px;
        }

        /* 6. BOTÃO (Gradiente Sutil) */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: transform 0.2s;
            width: 100%;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(118, 75, 162, 0.4);
        }

        /* 7. PROGRESS BAR */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_stylized_ui()

# ==========================================
# 🛠️ FUNÇÕES DO SISTEMA
# ==========================================
def gerar_nome_sequencial(categoria):
    pasta_destino = os.path.join("assets", "videos_prontos")
    os.makedirs(pasta_destino, exist_ok=True)
    arquivos_existentes = [f for f in os.listdir(pasta_destino) if f.startswith(categoria) and f.endswith(".mp4")]
    proximo_numero = len(arquivos_existentes) + 1
    return f"{categoria}_{proximo_numero}.mp4"

def mapear_tema(escolha):
    if "Cristão" in escolha: return "assets/background_cristao.mp4", "cristao"
    if "Musculação" in escolha: return "assets/background_musculacao.mp4", "musculacao"
    if "Música" in escolha: return "assets/background_musica.mp4", "musica"
    return "assets/background_minecraft.mp4", "aleatorio"

# ==========================================
# 🏭 INTERFACE PRINCIPAL
# ==========================================
st.title("Fábrica Quiz Mania")
st.markdown("Central de Produção Automatizada")

# ABAS
tab1, tab2, tab3 = st.tabs(["Vídeo 01", "Vídeo 02", "Vídeo 03"])

opcoes_temas = ["1 - Cristão / Teologia", "2 - Musculação / Fitness", "3 - Música / Instrumentos", "4 - Aleatório (Minecraft)"]

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        roteiro_1 = st.text_area("Roteiro JSON", height=120, key="json1", placeholder='Cole o JSON aqui...')
    with col2:
        st.write("") # Espaço vazio pra alinhar
        st.write("") 
        tema_1 = st.selectbox("Tema", opcoes_temas, key="tema1")

with tab2:
    col1, col2 = st.columns([3, 1])
    with col1:
        roteiro_2 = st.text_area("Roteiro JSON", height=120, key="json2", placeholder='Cole o JSON aqui...')
    with col2:
        st.write("") 
        st.write("") 
        tema_2 = st.selectbox("Tema", opcoes_temas, key="tema2")

with tab3:
    col1, col2 = st.columns([3, 1])
    with col1:
        roteiro_3 = st.text_area("Roteiro JSON", height=120, key="json3", placeholder='Cole o JSON aqui...')
    with col2:
        st.write("") 
        st.write("") 
        tema_3 = st.selectbox("Tema", opcoes_temas, key="tema3")

st.markdown("---")

# ==========================================
# 🚀 LÓGICA DE EXECUÇÃO
# ==========================================
if st.button("INICIAR PRODUÇÃO", type="primary"):
    
    fila = []
    inputs = [(roteiro_1, tema_1, "Vídeo 01"), (roteiro_2, tema_2, "Vídeo 02"), (roteiro_3, tema_3, "Vídeo 03")]
    
    for j, t, n in inputs:
        if j.strip(): fila.append((j, t, n))
            
    if not fila:
        st.warning("⚠️ Preencha pelo menos um roteiro.")
        st.stop()
        
    prog_bar = st.progress(0, text="Iniciando motores...")
    step = 1.0 / len(fila)
    
    for i, (json_txt, tema, nome) in enumerate(fila):
        try:
            base = i * step
            prog_bar.progress(base, text=f"⏳ {nome}: Lendo dados...")
            
            try:
                data = json.loads(json_txt)
                with open("quiz.json", "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False)
            except:
                st.error(f"Erro JSON no {nome}"); continue

            path_bg, cat = mapear_tema(tema)
            fname = gerar_nome_sequencial(cat)
            final_path = os.path.join("assets", "videos_prontos", fname)

            prog_bar.progress(base + (step*0.3), text=f"🎙️ {nome}: Gerando Voz...")
            quiz_audio = processar_vozes_do_quiz(data)
            
            prog_bar.progress(base + (step*0.6), text=f"🎬 {nome}: Renderizando...")
            gerar_video_final(quiz_audio, fname, path_bg)
            
            st.toast(f"{nome} Pronto!", icon="✅")
            with st.expander(f"▶️ Resultado: {nome}", expanded=True):
                st.video(final_path)
                
        except Exception as e:
            st.error(f"Erro {nome}: {e}")

    prog_bar.progress(100, text="✅ Processo Finalizado!")
    st.balloons()