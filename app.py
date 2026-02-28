import streamlit as st
import os
import json
import time
import glob
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
        .block-container {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        h1, h2, h3 { color: #ffffff !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; letter-spacing: -1px; }
        p, .stMarkdown { color: #b0b0b0 !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: rgba(0,0,0,0.2); padding: 5px; border-radius: 10px; }
        .stTabs [data-baseweb="tab"] { background-color: transparent; color: #888; border: none; border-radius: 8px; transition: all 0.3s; }
        .stTabs [aria-selected="true"] { background-color: #2d2d2d; color: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div { background-color: #0a0a0a; color: white; border: 1px solid #333; border-radius: 8px; }
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 0.75rem 1.5rem;
            border-radius: 8px; font-weight: 600; letter-spacing: 0.5px; transition: transform 0.2s; width: 100%;
        }
        div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(118, 75, 162, 0.4); }
        .stProgress > div > div > div > div { background: linear-gradient(90deg, #667eea, #764ba2); }
        </style>
        """,
        unsafe_allow_html=True
    )

set_stylized_ui()

# ==========================================
# 🛠️ FUNÇÕES DO SISTEMA
# ==========================================
PASTA_ASSETS = "assets"
os.makedirs(PASTA_ASSETS, exist_ok=True)

def obter_temas_dinamicos():
    temas = {}
    arquivos_mp4 = glob.glob(os.path.join(PASTA_ASSETS, "*.mp4"))
    for caminho in arquivos_mp4:
        nome_arquivo = os.path.basename(caminho)
        # Ignora arquivos que não são de background na hora de listar
        if nome_arquivo.startswith("background_"):
            nome_limpo = nome_arquivo.replace(".mp4", "").replace("background_", "").replace("_", " ").title()
            temas[nome_limpo] = caminho
    if not temas:
        temas["Nenhum vídeo encontrado"] = None
    return temas

def gerar_nome_sequencial(categoria):
    pasta_destino = os.path.join(PASTA_ASSETS, "videos_prontos")
    os.makedirs(pasta_destino, exist_ok=True)
    arquivos_existentes = [f for f in os.listdir(pasta_destino) if f.startswith(categoria) and f.endswith(".mp4")]
    proximo_numero = len(arquivos_existentes) + 1
    return f"{categoria}_{proximo_numero}.mp4"

# ==========================================
# 🏭 INTERFACE PRINCIPAL
# ==========================================
st.title("Fábrica Quiz Mania")
st.markdown("Central de Produção Automatizada")

dicionario_temas = obter_temas_dinamicos()
opcoes_temas = list(dicionario_temas.keys())

# Adicionada a 4ª aba: Gerenciar Temas
tab1, tab2, tab3, tab4 = st.tabs(["Vídeo 01", "Vídeo 02", "Vídeo 03", "⚙️ Gerenciar Temas"])

# --- ABAS DE PRODUÇÃO ---
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1: roteiro_1 = st.text_area("Roteiro JSON", height=120, key="json1", placeholder='Cole o JSON aqui...')
    with col2: st.write(""); st.write(""); tema_1 = st.selectbox("Tema", opcoes_temas, key="tema1")

with tab2:
    col1, col2 = st.columns([3, 1])
    with col1: roteiro_2 = st.text_area("Roteiro JSON", height=120, key="json2", placeholder='Cole o JSON aqui...')
    with col2: st.write(""); st.write(""); tema_2 = st.selectbox("Tema", opcoes_temas, key="tema2")

with tab3:
    col1, col2 = st.columns([3, 1])
    with col1: roteiro_3 = st.text_area("Roteiro JSON", height=120, key="json3", placeholder='Cole o JSON aqui...')
    with col2: st.write(""); st.write(""); tema_3 = st.selectbox("Tema", opcoes_temas, key="tema3")

# --- ABA DE GERENCIAMENTO DE TEMAS ---
with tab4:
    st.subheader("➕ Adicionar Novo Tema")
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        novo_video_upload = st.file_uploader("Upload do Vídeo de Fundo (MP4)", type=["mp4"])
    with col_t2:
        nome_novo_tema = st.text_input("Nome do Tema", placeholder="Ex: Curiosidades")
        
    if st.button("💾 Salvar Novo Tema", key="btn_salvar_tema"):
        if novo_video_upload and nome_novo_tema:
            # Formata o nome para o padrão correto do sistema
            nome_formatado = nome_novo_tema.strip().lower().replace(" ", "_")
            nome_arquivo_final = f"background_{nome_formatado}.mp4"
            caminho_salvar = os.path.join(PASTA_ASSETS, nome_arquivo_final)
            
            with open(caminho_salvar, "wb") as f:
                f.write(novo_video_upload.getbuffer())
                
            st.success(f"Tema '{nome_novo_tema}' adicionado com sucesso!")
            time.sleep(1)
            st.rerun() # Atualiza a página para o tema aparecer nas outras abas
        else:
            st.warning("Preencha o nome do tema e selecione um vídeo.")

    st.divider()
    
    st.subheader("🗑️ Remover Tema")
    tema_para_remover = st.selectbox("Selecione o tema para excluir", opcoes_temas, key="remover_tema")
    if st.button("Excluir Tema Selecionado", key="btn_excluir_tema"):
        if tema_para_remover and tema_para_remover != "Nenhum vídeo encontrado":
            caminho_remover = dicionario_temas[tema_para_remover]
            if os.path.exists(caminho_remover):
                os.remove(caminho_remover)
                st.success(f"Tema '{tema_para_remover}' excluído!")
                time.sleep(1)
                st.rerun() # Atualiza a página removendo o tema da lista

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

            path_bg = dicionario_temas[tema]
            if not path_bg:
                st.error(f"Erro: Fundo não encontrado para {tema}. Adicione na aba de Gerenciar Temas."); continue
                
            cat = tema.lower().replace(" ", "_")
            fname = gerar_nome_sequencial(cat)
            final_path = os.path.join(PASTA_ASSETS, "videos_prontos", fname)

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