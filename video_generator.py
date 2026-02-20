import os
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import *

# --- CONFIGURAÇÕES ---
LARGURA = 1080
ALTURA = 1920

# Cores
COR_CARD = (255, 255, 255)         
COR_BOTAO_BASE = (255, 0, 80)      # Vermelho
COR_BOTAO_CERTO = (0, 200, 100)    # Verde
COR_AMARELO = (255, 255, 0)

# Caminhos
FONTE_BOLD = "C:/Windows/Fonts/arialbd.ttf"
VIDEO_FUNDO = os.path.join("assets", "background.mp4")
IMG_FUNDO = os.path.join("assets", "fundo.jpg")
SOM_TIC_TAC = r"C:\Users\Micro\OneDrive\Documentos\projetos\quiz_ai\assets\ticking.mp3"
SOM_CORRETO = r"C:\Users\Micro\OneDrive\Documentos\projetos\quiz_ai\assets\correct.mp3"

# --- FUNÇÕES GRÁFICAS (PILLOW) ---

def carregar_fonte(tamanho):
    try:
        return ImageFont.truetype(FONTE_BOLD, tamanho)
    except:
        return ImageFont.load_default()

def criar_card_pergunta_integrado(texto_pergunta):
    """
    DESENHA O TEXTO DENTRO DO CARD.
    Isso centraliza matematicamente e impede cortes.
    """
    w_card, h_card = 900, 600
    radius = 60
    padding = 40
    
    # 1. Cria a imagem do card (transparente por fora)
    img = Image.new('RGBA', (w_card, h_card), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # 2. Desenha o fundo branco arredondado
    draw.rounded_rectangle((0, 0, w_card, h_card), radius=radius, fill=COR_CARD)
    
    # 3. Configura a fonte
    tamanho_fonte = 60
    font = carregar_fonte(tamanho_fonte)
    
    # 4. Quebra o texto (Word Wrap manual) para caber na largura
    # Calcula quantos caracteres cabem aprox (ajuste empírico baseada no tamanho 60)
    chars_por_linha = 22 
    linhas = textwrap.wrap(texto_pergunta.upper(), width=chars_por_linha)
    
    # 5. Calcula altura total do bloco de texto para centralizar verticalmente
    # bbox(left, top, right, bottom)
    alturas_linhas = []
    for linha in linhas:
        bbox = draw.textbbox((0, 0), linha, font=font)
        alturas_linhas.append(bbox[3] - bbox[1])
    
    espaco_entrelinhas = 15
    altura_total_texto = sum(alturas_linhas) + (espaco_entrelinhas * (len(linhas) - 1))
    
    # Ponto Y inicial para ficar EXATAMENTE no meio
    y_atual = (h_card - altura_total_texto) / 2
    
    # 6. Desenha linha por linha
    for i, linha in enumerate(linhas):
        bbox = draw.textbbox((0, 0), linha, font=font)
        largura_texto = bbox[2] - bbox[0]
        x_atual = (w_card - largura_texto) / 2
        
        draw.text((x_atual, y_atual), linha, font=font, fill='black')
        y_atual += alturas_linhas[i] + espaco_entrelinhas
        
    return ImageClip(np.array(img)).with_position(('center', 200))

def criar_botao_pillow(texto, letra, cor_fundo, y_pos):
    """Botão desenhado pixel a pixel no Pillow"""
    w_btn, h_btn = 900, 220
    img = Image.new('RGBA', (w_btn, h_btn), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Base
    draw.rounded_rectangle((0,0, w_btn, h_btn), radius=50, fill=cor_fundo)
    
    # Box Letra (Branco)
    box_size = 160
    margin_left = 30
    y_box = (h_btn - box_size) // 2
    draw.rounded_rectangle((margin_left, y_box, margin_left+box_size, y_box+box_size), radius=30, fill='white')
    
    # Letra (A, B, C)
    font_letra = carregar_fonte(80)
    bbox = draw.textbbox((0,0), letra, font=font_letra)
    w_txt = bbox[2] - bbox[0]
    h_txt = bbox[3] - bbox[1]
    # Centraliza no box branco
    x_letra = margin_left + (box_size - w_txt) / 2
    y_letra = y_box + (box_size - h_txt) / 2 - 10 # ajuste fino baseline
    draw.text((x_letra, y_letra), letra, font=font_letra, fill=cor_fundo)
    
    # Texto Resposta
    font_resp = carregar_fonte(45)
    # Wrap simples para resposta não vazar
    linhas_resp = textwrap.wrap(texto, width=28) 
    
    x_resp = 230
    # Calcula Y inicial para centralizar
    total_h_resp = 0
    bboxes_resp = []
    for line in linhas_resp:
        bb = draw.textbbox((0,0), line, font=font_resp)
        h_line = bb[3] - bb[1]
        bboxes_resp.append(h_line)
        total_h_resp += h_line
    
    y_resp_start = (h_btn - total_h_resp - (10 * (len(linhas_resp)-1))) / 2
    
    for i, line in enumerate(linhas_resp):
        draw.text((x_resp, y_resp_start), line, font=font_resp, fill='white')
        y_resp_start += bboxes_resp[i] + 10

    return ImageClip(np.array(img)).with_position(('center', y_pos))

def criar_timer_pillow(numero):
    """Cria o número em uma imagem GRANDE transparente para não cortar"""
    size = 400 # Canvas grande
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    font = carregar_fonte(200)
    text = str(numero)
    
    # Desenha Stroke (Borda preta manual)
    bbox = draw.textbbox((0,0), text, font=font)
    w_txt = bbox[2] - bbox[0]
    h_txt = bbox[3] - bbox[1]
    
    x = (size - w_txt) / 2
    y = (size - h_txt) / 2 - 20
    
    # Simula borda desenhando várias vezes deslocado
    stroke_width = 8
    for offx in range(-stroke_width, stroke_width+1):
        for offy in range(-stroke_width, stroke_width+1):
            draw.text((x+offx, y+offy), text, font=font, fill='black')
            
    # Desenha miolo amarelo
    draw.text((x, y), text, font=font, fill=COR_AMARELO)
    
    # Retorna clipe posicionado bem em cima da área segura
    return ImageClip(np.array(img)).with_position(('center', 1500))

# --- LÓGICA DE VÍDEO ---

def criar_clip_pergunta(dados_pergunta, numero, clip_fundo_base):
    if "audio_path" not in dados_pergunta: return None

    # Tempos
    audio_voz = AudioFileClip(dados_pergunta["audio_path"])
    tempo_leitura = audio_voz.duration
    tempo_pensar = 5.0 
    tempo_resposta = 2.0
    duracao_total = tempo_leitura + tempo_pensar + tempo_resposta

    # Camadas
    fundo = clip_fundo_base.with_duration(duracao_total)
    
    # 1. Card Pergunta (Novo método integrado)
    clip_card = criar_card_pergunta_integrado(dados_pergunta['pergunta'])
    clip_card = clip_card.with_duration(duracao_total)

    # 2. Botões
    clips_botoes = []
    y_start = 850
    gap = 260

    for i, opcao in enumerate(dados_pergunta['opcoes']):
        eh_correta = (i == dados_pergunta['correta'])
        letra = ['A', 'B', 'C'][i]
        
        btn_normal = criar_botao_pillow(opcao, letra, COR_BOTAO_BASE, y_start + (i*gap))
        btn_normal = btn_normal.with_duration(tempo_leitura + tempo_pensar)
        
        cor_final = COR_BOTAO_CERTO if eh_correta else COR_BOTAO_BASE
        btn_final = criar_botao_pillow(opcao, letra, cor_final, y_start + (i*gap))
        btn_final = btn_final.with_start(tempo_leitura + tempo_pensar).with_duration(tempo_resposta)

        # Animação Pulo
        if eh_correta:
             btn_final = btn_final.resized(lambda t: 1.0 + 0.05 * np.sin(t * 10)) # Pulso mais rápido

        clips_botoes.append(btn_normal)
        clips_botoes.append(btn_final)

    # 3. Timer (Novo método Pillow)
    clips_timer = []
    for t in range(5, 0, -1):
        start_time = tempo_leitura + (5 - t)
        clip_num = criar_timer_pillow(t).with_start(start_time).with_duration(1)
        clips_timer.append(clip_num)

    # Áudio
    audios = [audio_voz]
    if os.path.exists(SOM_TIC_TAC):
        try:
            tic_tac_base = AudioFileClip(SOM_TIC_TAC).with_volume_scaled(0.5)
            loops = int(tempo_pensar / tic_tac_base.duration) + 2
            tic_tac_loop = concatenate_audioclips([tic_tac_base] * loops)
            tic_tac_final = tic_tac_loop.subclipped(0, tempo_pensar).with_start(tempo_leitura)
            audios.append(tic_tac_final)
        except: pass

    if os.path.exists(SOM_CORRETO):
        try:
            som_ok = AudioFileClip(SOM_CORRETO).with_start(tempo_leitura + tempo_pensar)
            audios.append(som_ok)
        except: pass

    audio_final = CompositeAudioClip(audios)

    # Montagem
    camadas = [fundo, clip_card] + clips_botoes + clips_timer
    return CompositeVideoClip(camadas).with_audio(audio_final).with_duration(duracao_total)

def gerar_video_final(quiz_data, nome_arquivo="quiz_v9_perfect.mp4"):
    print("\n--- 🎬 Renderizando V9 (Layout Matemático) ---")
    
    # Fundo
    clip_bg = None
    if os.path.exists(VIDEO_FUNDO):
        try:
            bg = VideoFileClip(VIDEO_FUNDO).without_audio()
            clip_bg = bg.resized(height=ALTURA).cropped(x1=bg.resized(height=ALTURA).w/2 - LARGURA/2, width=LARGURA, height=ALTURA)
        except: pass
    
    if clip_bg is None:
        clip_bg = ColorClip(size=(LARGURA, ALTURA), color=(30, 30, 30))

    clips_finais = []
    tempo_acumulado = 0
    
    for i, item in enumerate(quiz_data):
        print(f"🔨 Q{i+1}: Desenhando...")
        bg_da_vez = clip_bg
        if isinstance(clip_bg, VideoFileClip) and clip_bg.duration:
            inicio = tempo_acumulado % clip_bg.duration
            bg_da_vez = clip_bg.subclipped(inicio, clip_bg.duration)
            
        clip = criar_clip_pergunta(item, i+1, bg_da_vez)
        if clip:
            clips_finais.append(clip)
            tempo_acumulado += clip.duration

    if not clips_finais: return

    print("🚀 Concatenando...")
    final = concatenate_videoclips(clips_finais, method="compose")
    caminho = os.path.join("assets", nome_arquivo)
    # Preset medium para garantir qualidade
    final.write_videofile(caminho, fps=24, codec='libx264', audio_codec='aac', preset='medium') 
    print(f"✅ VÍDEO PRONTO: {caminho}")

if __name__ == "__main__":
    pass