import sys
import asyncio
import nest_asyncio

# Aplica a vacina para permitir múltiplos motores rodando juntos (Edge TTS + Playwright)
nest_asyncio.apply()

# Corrige o erro do Playwright/TikTok no Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import os
import json
import time
import glob
from uploader import fazer_upload_youtube
from uploader_tiktok import fazer_upload_tiktok
from voice_generator import processar_vozes_do_quiz, processar_voz_vendas
from video_generator import gerar_video_final
from video_generator_vendas import gerar_video_vendas
from gerador_roteiros import gerar_trinca_quiz_mania # <--- O CÉREBRO NOVO IMPORTADO AQUI

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Fábrica Automática 2 em 1", page_icon="⚡", layout="centered")

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
st.title("Fábrica Automática 2 em 1 ⚡")

dicionario_temas = obter_temas_dinamicos()
opcoes_temas = list(dicionario_temas.keys())

# --- 1. MENU LATERAL (A CHAVE SELETORA) ---
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    modo_operacao = st.radio(
        "Selecione a Linha de Produção:",
        ["Modo Quiz Mania 🧠", "Modo Vendas (Review) 💰"]
    )
    
    st.markdown("---")
    st.write("🌐 Configurações de Postagem:")
    publicar_auto = st.checkbox("🚀 Publicar no YouTube", value=True)
    publicar_tiktok = st.checkbox("🎵 Publicar no TikTok", value=True)
    
    # ==========================================
    # 🔗 CAIXAS DE DESCRIÇÕES FIXAS
    # ==========================================
    st.markdown("---")
    st.write("🔗 Links de Afiliado e Descrições:")
    with st.expander("Configurar Textos Fixos (Quiz)", expanded=False):
        desc_crist = st.text_area(
            "Texto - Cristianismo:", 
            value="Comente quantas você acertou! E não esquece de seguir para mais curiosidades diárias. 👇\n\nQUER UM VIOLÃO? Cole este ID no buscador do Mercado Livre: 8F1V1F-HXXC\n\n🔗 Ou acesse este link:\nhttps://meli.la/1ym5joa\n\n#quiz #curiosidades #shorts"
        )
        desc_musc = st.text_area(
            "Texto - Musculação:", 
            value="Comente quantas você acertou! E não esquece de seguir para mais curiosidades diárias. 👇\n\nA creatina mais pura do mercado com desconto! Pegue aqui: https://sua-loja.com/creatina\n\n#academia #creatina #treino #shorts"
        )
        desc_musica = st.text_area(
            "Texto - Música:", 
            value="Comente quantas você acertou! E não esquece de seguir para mais curiosidades diárias. 👇\n\nQUER UM VIOLÃO? Cole este ID no buscador do Mercado Livre: 8F1V1F-HXXC\n\n🔗 Ou acesse este link:\nhttps://meli.la/1ym5joa\n\n#quiz #musica #violao #shorts"
        )
    # ==========================================

    st.markdown("---")
    st.write("🔧 Ferramentas de Manutenção:")
    if st.button("🧹 Limpar Token YouTube (Corrige Erro)"):
        apagou = False
        arquivos_token = ["token.pickle", "token.json", ".oauth-credentials"]
        for arquivo in arquivos_token:
            if os.path.exists(arquivo):
                os.remove(arquivo)
                apagou = True
        
        if apagou:
            st.success("✅ Tokens antigos apagados! Na próxima postagem o navegador vai abrir para você logar no Google de novo.")
        else:
            st.info("Nenhum token encontrado na pasta.")


# ==========================================
# 🧠 MODO 1: FÁBRICA DE QUIZ
# ==========================================
if modo_operacao == "Modo Quiz Mania 🧠":
    st.markdown("### 🧠 Central de Produção: Quiz")
    
    # --- ADICIONADO AQUI: A CHAVE DE MODO ---
    metodo_entrada = st.radio("Como você quer gerar os roteiros hoje?", ["🤖 Modo IA (Gerar Automático)", "✍️ Modo Manual (Colar JSON)"], horizontal=True)
    st.markdown("---")

    if metodo_entrada == "🤖 Modo IA (Gerar Automático)":
        st.info("A IA vai escrever a trinca de ouro (Cristianismo, Musculação e Música). Selecione os vídeos de fundo para cada um:")
        
        col_bg1, col_bg2, col_bg3 = st.columns(3)
        with col_bg1: bg_crist = st.selectbox("Fundo 1 (Cristianismo)", opcoes_temas, key="bg_c")
        with col_bg2: bg_musc = st.selectbox("Fundo 2 (Musculação)", opcoes_temas, key="bg_m")
        with col_bg3: bg_musica = st.selectbox("Fundo 3 (Música)", opcoes_temas, key="bg_mu")

        if not st.session_state.get('rodando', False):
            if st.button("🤖 GERAR ROTEIROS E LIGAR MÁQUINA", type="primary"):
                with st.spinner("🧠 O Gemini está escrevendo os roteiros e injetando seus links..."):
                    trinca_json = gerar_trinca_quiz_mania(desc_crist, desc_musc, desc_musica)
                
                if trinca_json and len(trinca_json) == 3:
                    st.session_state.fila_quiz = [
                        (json.dumps(trinca_json[0]), bg_crist, "Quiz 01 - Cristianismo"),
                        (json.dumps(trinca_json[1]), bg_musc, "Quiz 02 - Musculação"),
                        (json.dumps(trinca_json[2]), bg_musica, "Quiz 03 - Música")
                    ]
                    st.session_state.indice_quiz = 0
                    st.session_state.rodando = True
                    st.rerun()
                else:
                    st.error("❌ Erro ao gerar os roteiros. Verifique sua chave de API.")
                    
    else: # MODO MANUAL ORIGINAL INTACTO
        tab1, tab2, tab3, tab4 = st.tabs(["Vídeo 01", "Vídeo 02", "Vídeo 03", "⚙️ Gerenciar Temas"])

        with tab1:
            col1, col2 = st.columns([3, 1])
            with col1: 
                roteiro_1 = st.text_area("JSON Completo (Título, Descrição e Perguntas)", height=250, key="json1", placeholder='Cole o JSON Mestre aqui...')
            with col2: 
                st.write(""); st.write(""); tema_1 = st.selectbox("Tema", opcoes_temas, key="tema1")

        with tab2:
            col1, col2 = st.columns([3, 1])
            with col1: 
                roteiro_2 = st.text_area("JSON Completo (Título, Descrição e Perguntas)", height=250, key="json2", placeholder='Cole o JSON Mestre aqui...')
            with col2: 
                st.write(""); st.write(""); tema_2 = st.selectbox("Tema", opcoes_temas, key="tema2")

        with tab3:
            col1, col2 = st.columns([3, 1])
            with col1: 
                roteiro_3 = st.text_area("JSON Completo (Título, Descrição e Perguntas)", height=250, key="json3", placeholder='Cole o JSON Mestre aqui...')
            with col2: 
                st.write(""); st.write(""); tema_3 = st.selectbox("Tema", opcoes_temas, key="tema3")

        with tab4:
            st.subheader("➕ Adicionar Novo Tema")
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                novo_video_upload = st.file_uploader("Upload do Vídeo de Fundo (MP4)", type=["mp4"])
            with col_t2:
                nome_novo_tema = st.text_input("Nome do Tema", placeholder="Ex: Curiosidades")
                
            if st.button("💾 Salvar Novo Tema", key="btn_salvar_tema"):
                if novo_video_upload and nome_novo_tema:
                    nome_formatado = nome_novo_tema.strip().lower().replace(" ", "_")
                    nome_arquivo_final = f"background_{nome_formatado}.mp4"
                    caminho_salvar = os.path.join(PASTA_ASSETS, nome_arquivo_final)
                    
                    with open(caminho_salvar, "wb") as f:
                        f.write(novo_video_upload.getbuffer())
                        
                    st.success(f"Tema '{nome_novo_tema}' adicionado com sucesso!")
                    time.sleep(1)
                    st.rerun() 
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
                        st.rerun() 

    # --- LÓGICA DE EXECUÇÃO DO QUIZ (AUTOMÁTICA COM PAUSA) ---
    st.markdown("---")
    st.subheader("⚙️ Controle da Esteira (Quiz)")

    # Cria a memória de estado (o cérebro da esteira)
    if "fila_quiz" not in st.session_state:
        st.session_state.fila_quiz = []
    if "indice_quiz" not in st.session_state:
        st.session_state.indice_quiz = 0
    if "rodando" not in st.session_state:
        st.session_state.rodando = False

    col_b1, col_b2, col_b3 = st.columns(3)

    with col_b1:
        # Se não estiver rodando E estiver no modo manual, mostra o botão de iniciar
        if not st.session_state.rodando and metodo_entrada == "✍️ Modo Manual (Colar JSON)":
            if st.button("▶️ INICIAR PRODUÇÃO MANUAL", type="primary"):
                inputs = [(roteiro_1, tema_1, "Vídeo 01"), (roteiro_2, tema_2, "Vídeo 02"), (roteiro_3, tema_3, "Vídeo 03")]
                st.session_state.fila_quiz = [i for i in inputs if i[0].strip()]
                st.session_state.indice_quiz = 0
                
                if not st.session_state.fila_quiz:
                    st.warning("⚠️ Preencha pelo menos um roteiro antes de iniciar.")
                else:
                    st.session_state.rodando = True
                    st.rerun() # Dispara a máquina!

    with col_b2:
        # Mostra o botão PAUSAR se a máquina estiver ligada
        if st.session_state.rodando:
            if st.button("⏸️ PAUSAR MÁQUINA"):
                st.session_state.rodando = False
                st.warning("⚠️ Pausando... A máquina vai parar assim que terminar o vídeo atual.")
                st.rerun()
        # Mostra o botão RETOMAR se a máquina estiver pausada no meio do caminho
        elif st.session_state.indice_quiz > 0 and st.session_state.indice_quiz < len(st.session_state.fila_quiz):
            if st.button("▶️ RETOMAR DE ONDE PAROU"):
                st.session_state.rodando = True
                st.rerun()

    with col_b3:
        if st.button("⏹️ CANCELAR TUDO"):
            st.session_state.fila_quiz = []
            st.session_state.indice_quiz = 0
            st.session_state.rodando = False
            st.error("🚨 Parada de emergência acionada. Fila zerada.")
            st.rerun()

    # ==========================================
    # O MOTOR (Processa 1 por vez e reinicia sozinho)
    # ==========================================
    if st.session_state.rodando and st.session_state.indice_quiz < len(st.session_state.fila_quiz):
        
        json_txt, tema, nome = st.session_state.fila_quiz[st.session_state.indice_quiz]
        
        st.markdown(f"### 🚧 Trabalhando agora no: {nome}")
        prog_bar = st.progress(0, text="Iniciando motores...")
        
        try:
            prog_bar.progress(10, text=f"⏳ {nome}: Lendo dados do JSON...")
            data = json.loads(json_txt)
            if isinstance(data, dict):
                titulo_json = data.get("titulo", "")
                desc_json = data.get("descricao", "")
                perguntas_quiz = data.get("perguntas", [])
            else:
                titulo_json = ""
                desc_json = ""
                perguntas_quiz = data
            
            with open("quiz.json", "w", encoding="utf-8") as f: 
                json.dump(perguntas_quiz, f, ensure_ascii=False)

            path_bg = dicionario_temas[tema]
            if not path_bg:
                st.error(f"Erro: Fundo não encontrado para {tema}. Adicione na aba de Gerenciar Temas.")
                st.session_state.rodando = False
            else:
                cat = tema.lower().replace(" ", "_")
                fname = gerar_nome_sequencial(cat)
                final_path = os.path.join(PASTA_ASSETS, "videos_prontos", fname)

                prog_bar.progress(30, text=f"🎙️ {nome}: Gerando Voz...")
                quiz_audio = processar_vozes_do_quiz(perguntas_quiz)
                
                prog_bar.progress(60, text=f"🎬 {nome}: Renderizando...")
                gerar_video_final(quiz_audio, fname, path_bg)
                
                titulo_final = titulo_json.strip() if titulo_json.strip() else f"Quiz de {tema.title()} - Consegue acertar?"
                if "#shorts" not in titulo_final.lower():
                    titulo_final += " #shorts"
                    
                desc_final = desc_json.strip() if desc_json.strip() else f"Deixe nos comentários quantas respostas acertou! 👇\n\n#quiz #{tema.lower().replace(' ', '')} #shorts"
                tags_video = ["quiz", "conhecimento", "curiosidades", "shorts", tema.lower()]

                if publicar_auto:
                    prog_bar.progress(80, text=f"🚀 {nome}: Enviando para o YouTube...")
                    fazer_upload_youtube(final_path, titulo_final, desc_final, tags_video)
                
                if publicar_tiktok:
                    prog_bar.progress(90, text=f"🎵 {nome}: Enviando para o TikTok...")
                    fazer_upload_tiktok(final_path, desc_final)
                
                prog_bar.progress(100, text=f"✅ {nome} Finalizado!")
                st.video(final_path)
                
                # O PULO DO GATO: Avança o índice e recarrega a página automaticamente!
                st.session_state.indice_quiz += 1
                
                if st.session_state.indice_quiz < len(st.session_state.fila_quiz):
                    st.toast(f"Indo para o próximo vídeo...")
                    time.sleep(2) # Pausa de 2 segundos para você respirar
                    st.rerun() # Dispara o próximo da fila automaticamente!
                else:
                    st.session_state.rodando = False
                    st.success("🔥 Todos os vídeos da fila foram concluídos com sucesso!")
                    st.balloons()
                
        except Exception as e:
            st.error(f"Erro no {nome}: {e}")
            st.session_state.rodando = False
            if "invalid_grant" in str(e).lower():
                st.error("🚨 O token do YouTube expirou! Vá no menu lateral esquerdo e clique no botão 'Limpar Token YouTube'.")


# ==========================================
# 💰 MODO 2: FÁBRICA DE VENDAS (REVIEW)
# ==========================================
elif modo_operacao == "Modo Vendas (Review) 💰":
    st.markdown("### 💰 Central de Produção: Máquina de Vendas Rápida")
    
    col_v1, col_v2 = st.columns([3, 1])
    with col_v1:
        roteiro_vendas = st.text_area("JSON de Vendas (Cenas e Tempos)", height=250, placeholder='Cole o JSON Mestre de Vendas aqui...')
    with col_v2:
        st.write(""); st.write("")
        pasta_broll = st.selectbox("Pasta de B-Roll (Fundo)", ["violao", "creatina", "geral"])
        
    st.markdown("---")
    
    if st.button("INICIAR PRODUÇÃO DE VENDAS", type="primary"):
        if not roteiro_vendas.strip():
            st.warning("⚠️ Cola o JSON do teu vídeo de vendas antes de continuar.")
            st.stop()
            
        prog_bar = st.progress(0, text="A iniciar o motor de vendas...")
        
        try:
            # 1. Lê o JSON
            prog_bar.progress(10, text="A ler o guião de vendas...")
            dados_vendas = json.loads(roteiro_vendas)
            titulo_vendas = dados_vendas.get("titulo_youtube", "Review Incrível! #shorts")
            desc_vendas = dados_vendas.get("descricao_links", "Vê o link nos comentários!")
            cenas = dados_vendas.get("cenas", [])
            
            # 2. Gera a Voz
            prog_bar.progress(30, text="🎙️ A gerar a locução de alta conversão...")
            caminho_audio_vendas = processar_voz_vendas(cenas)
            
            # 3. Renderiza o Vídeo
            prog_bar.progress(60, text="🎬 A renderizar o vídeo com legendas dinâmicas...")
            nome_video_saida = f"venda_{pasta_broll}_{int(time.time())}.mp4"
            caminho_video_final = gerar_video_vendas(caminho_audio_vendas, nome_video_saida, pasta_broll, cenas)
            
            # 4. Dispara para as Redes
            tags_vendas = ["review", "vale a pena", "dica", "shorts", pasta_broll]
            
            if publicar_auto:
                prog_bar.progress(80, text="🚀 A enviar para o YouTube Shorts...")
                fazer_upload_youtube(caminho_video_final, titulo_vendas, desc_vendas, tags_vendas)
                st.toast("Publicado no YouTube!", icon="🚀")
                
            if publicar_tiktok:
                prog_bar.progress(90, text="🎵 A despachar para o TikTok...")
                fazer_upload_tiktok(caminho_video_final, desc_vendas)
                st.toast("Publicado no TikTok!", icon="🎵")
                
            prog_bar.progress(100, text="✅ Máquina de Vendas Finalizada!")
            st.balloons()
            
            with st.expander("▶️ Ver o Vídeo de Vendas Pronto", expanded=True):
                st.video(caminho_video_final)
                
        except Exception as e:
            st.error(f"Ocorreu um erro na produção: {e}")
            if "invalid_grant" in str(e).lower():
                st.error("🚨 O token do YouTube expirou! Vá no menu lateral esquerdo e clique no botão 'Limpar Token YouTube'.")