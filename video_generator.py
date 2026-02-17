import os
from moviepy import *
from moviepy.video.tools.subtitles import SubtitlesClip

# Configurações de layout (Vertical Full HD)
LARGURA = 1080
ALTURA = 1920
COR_FUNDO = (20, 20, 30) # Azul escuro quase preto
COR_TEXTO = 'white'
COR_DESTAQUE = 'green'
# Aponta direto para o arquivo da fonte no Windows
FONTE = "C:/Windows/Fonts/arial.ttf" # Se der erro de fonte, troque para 'clean' ou outra instalada

def quebrar_texto(texto, limite=30):
    """Quebra o texto em linhas para caber na tela vertical"""
    palavras = texto.split()
    linhas = []
    linha_atual = []
    
    for palavra in palavras:
        if len(" ".join(linha_atual + [palavra])) <= limite:
            linha_atual.append(palavra)
        else:
            linhas.append(" ".join(linha_atual))
            linha_atual = [palavra]
    linhas.append(" ".join(linha_atual))
    return "\n".join(linhas)

def criar_clip_pergunta(dados_pergunta, numero):
    """
    Cria um clipe de vídeo para UMA pergunta.
    Retorna um CompositeVideoClip.
    """
    # 1. Carrega o Áudio
    if "audio_path" not in dados_pergunta:
        print(f"⚠️ Pulei Q{numero} (sem áudio)")
        return None

    audio_clip = AudioFileClip(dados_pergunta["audio_path"])
    duracao_audio = audio_clip.duration
    
    # Tempo total do clipe = Áudio + 2 segundos para mostrar a resposta
    duracao_total = duracao_audio + 2.0

    # 2. Fundo (Cor sólida)
    fundo = ColorClip(size=(LARGURA, ALTURA), color=COR_FUNDO, duration=duracao_total)

    # 3. Texto da Pergunta (Topo)
    texto_perg = f"Quiz #{numero}\n\n{quebrar_texto(dados_pergunta['pergunta'])}"
    clip_pergunta = TextClip(
        text=texto_perg,
        font=FONTE,
        font_size=70,
        color=COR_TEXTO,
        method='caption',
        size=(LARGURA - 100, None),
        text_align='center'
    ).with_position(('center', 300)).with_duration(duracao_total)

    # 4. Opções
    clips_opcoes = []
    y_inicial = 900
    espacamento = 150

    for i, opcao in enumerate(dados_pergunta['opcoes']):
        # Se for o momento final (pós áudio) e for a correta, pinta de verde
        eh_a_correta = (i == dados_pergunta['correta'])
        
        # Texto normal (durante o áudio)
        txt_normal = TextClip(
            text=f"{['A','B','C'][i]}) {opcao}",
            font=FONTE,
            font_size=50,
            color=COR_TEXTO,
            text_align='left',
            size=(LARGURA - 200, None)
        ).with_position(('center', y_inicial + (i * espacamento))).with_duration(duracao_audio)

        # Texto destaque (após o áudio - só aparece a correta ou todas?)
        # Vamos fazer simples: A correta fica verde nos 2 segundos finais
        cor_final = COR_DESTAQUE if eh_a_correta else 'gray'
        
        txt_final = TextClip(
            text=f"{['A','B','C'][i]}) {opcao}",
            font=FONTE,
            font_size=55 if eh_a_correta else 50, # Aumenta um pouco a correta
            color=cor_final,
            text_align='left', # Ajuste aqui
             size=(LARGURA - 200, None)
        ).with_position(('center', y_inicial + (i * espacamento))).with_start(duracao_audio).with_duration(2.0)

        clips_opcoes.append(txt_normal)
        clips_opcoes.append(txt_final)

    # 5. Montagem
    final = CompositeVideoClip([fundo, clip_pergunta] + clips_opcoes)
    final = final.with_audio(audio_clip) # O áudio acaba antes do vídeo (efeito silêncio na resposta)
    
    return final

def gerar_video_final(quiz_data, nome_arquivo_saida="video_final.mp4"):
    print("\n--- 🎬 Iniciando Renderização do Vídeo ---")
    
    clips_perguntas = []
    
    for i, item in enumerate(quiz_data):
        print(f"🔨 Montando clipe da pergunta {i+1}...")
        clip = criar_clip_pergunta(item, i+1)
        if clip:
            clips_perguntas.append(clip)

    if not clips_perguntas:
        print("❌ Nenhum clipe foi gerado.")
        return

    # Junta todas as perguntas em um vídeo só
    video_completo = concatenate_videoclips(clips_perguntas, method="compose")
    
    caminho_saida = os.path.join("assets", nome_arquivo_saida)
    
    print(f"🚀 Renderizando vídeo final em: {caminho_saida}")
    print("Isso pode demorar alguns minutos dependendo do seu PC...")
    
    video_completo.write_videofile(
        caminho_saida, 
        fps=24, 
        codec='libx264', 
        audio_codec='aac'
    )
    
    print("✅ Vídeo renderizado com sucesso!")