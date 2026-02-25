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
COR_BOTAO_BASE = (255, 0, 80)      
COR_BOTAO_CERTO = (0, 200, 100)    
COR_AMARELO = (255, 255, 0)

# Caminhos das Fontes
# arialbd.ttf é boa para texto, mas não tem emoji.
FONTE_BOLD = "C:/Windows/Fonts/arialbd.ttf"
# seguiemj.ttf é a fonte do Windows que tem os emojis desenhados
FONTE_EMOJI = "C:/Windows/Fonts/seguiemj.ttf"

# Ajuste se necessário ou remova se não usar imagem estática
IMG_FUNDO = os.path.join("assets", "fundo.jpg") 

# Áudios
SOM_TIC_TAC = os.path.join("assets", "ticking.mp3")
SOM_CORRETO = os.path.join("assets", "correct.mp3")
SOM_FUNDO = os.path.join("assets", "background_music.mp3") 
SOM_ENCERRAMENTO = os.path.join("assets", "audio", "encerramento.mp3") 

# --- FUNÇÕES GRÁFICAS (PILLOW) ---
def carregar_fonte(tamanho, usa_emoji=False):
    caminho_fonte = FONTE_EMOJI if usa_emoji else FONTE_BOLD
    try: 
        return ImageFont.truetype(caminho_fonte, tamanho)
    except: 
        # Tenta fallback se a fonte específica não existir
        try:
            return ImageFont.truetype("arial.ttf", tamanho)
        except:
            return ImageFont.load_default()

def criar_card_pergunta_integrado(texto_pergunta):
    w_card, h_card = 900, 600
    radius = 60
    
    img = Image.new('RGBA', (w_card, h_card), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, w_card, h_card), radius=radius, fill=COR_CARD)
    
    font = carregar_fonte(60)
    linhas = textwrap.wrap(texto_pergunta.upper(), width=22)
    
    alturas_linhas = [draw.textbbox((0, 0), linha, font=font)[3] - draw.textbbox((0, 0), linha, font=font)[1] for linha in linhas]
    altura_total_texto = sum(alturas_linhas) + (15 * (len(linhas) - 1))
    
    y_atual = (h_card - altura_total_texto) / 2
    for i, linha in enumerate(linhas):
        largura_texto = draw.textbbox((0, 0), linha, font=font)[2] - draw.textbbox((0, 0), linha, font=font)[0]
        x_atual = (w_card - largura_texto) / 2
        draw.text((x_atual, y_atual), linha, font=font, fill='black')
        y_atual += alturas_linhas[i] + 15
        
    return ImageClip(np.array(img)).with_position(('center', 200))

def criar_botao_pillow(texto, letra, cor_fundo, y_pos):
    w_btn, h_btn = 900, 220
    img = Image.new('RGBA', (w_btn, h_btn), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    draw.rounded_rectangle((0,0, w_btn, h_btn), radius=50, fill=cor_fundo)
    
    box_size, margin_left = 160, 30
    y_box = (h_btn - box_size) // 2
    draw.rounded_rectangle((margin_left, y_box, margin_left+box_size, y_box+box_size), radius=30, fill='white')
    
    font_letra = carregar_fonte(80)
    bbox = draw.textbbox((0,0), letra, font=font_letra)
    x_letra = margin_left + (box_size - (bbox[2] - bbox[0])) / 2
    y_letra = y_box + (box_size - (bbox[3] - bbox[1])) / 2 - 10 
    draw.text((x_letra, y_letra), letra, font=font_letra, fill=cor_fundo)
    
    font_resp = carregar_fonte(45)
    linhas_resp = textwrap.wrap(texto, width=28) 
    
    bboxes_resp = [draw.textbbox((0,0), line, font=font_resp)[3] - draw.textbbox((0,0), line, font=font_resp)[1] for line in linhas_resp]
    y_resp_start = (h_btn - sum(bboxes_resp) - (10 * (len(linhas_resp)-1))) / 2
    
    for i, line in enumerate(linhas_resp):
        draw.text((230, y_resp_start), line, font=font_resp, fill='white')
        y_resp_start += bboxes_resp[i] + 10

    return ImageClip(np.array(img)).with_position(('center', y_pos))

def criar_timer_pillow(numero):
    size = 400 
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    font = carregar_fonte(200)
    text = str(numero)
    
    bbox = draw.textbbox((0,0), text, font=font)
    x, y = (size - (bbox[2] - bbox[0])) / 2, (size - (bbox[3] - bbox[1])) / 2 - 20
    
    for offx in range(-8, 9):
        for offy in range(-8, 9):
            draw.text((x+offx, y+offy), text, font=font, fill='black')
            
    draw.text((x, y), text, font=font, fill=COR_AMARELO)
    return ImageClip(np.array(img)).with_position(('center', 1500))

def criar_clip_encerramento(clip_fundo_base):
    duracao_final = 3.5 
    audio_encerramento = None
    
    if os.path.exists(SOM_ENCERRAMENTO):
        try:
            audio_encerramento = AudioFileClip(SOM_ENCERRAMENTO)
            duracao_final = max(3.5, audio_encerramento.duration + 0.5)
        except Exception as e:
            print(f"⚠️ Erro no áudio de encerramento: {e}")

    fundo = clip_fundo_base.with_duration(duracao_final)
    
    img = Image.new('RGBA', (LARGURA, ALTURA), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    w_card, h_card = 900, 700
    x_card, y_card = (LARGURA - w_card) // 2, (ALTURA - h_card) // 2
    draw.rounded_rectangle((x_card, y_card, x_card+w_card, y_card+h_card), radius=60, fill=COR_CARD)
    
    # Carregamos a fonte normal para títulos e a fonte de EMOJI para as frases de baixo
    font_grande = carregar_fonte(90)
    font_media_emoji = carregar_fonte(60, usa_emoji=True) # <--- AQUI A MÁGICA
    
    def txt_centro(texto, y, font, cor):
        x = (LARGURA - (draw.textbbox((0, 0), texto, font=font)[2] - draw.textbbox((0, 0), texto, font=font)[0])) / 2
        draw.text((x, y), texto, font=font, fill=cor)

    txt_centro("QUANTAS VOCÊ", y_card + 100, font_grande, 'black')
    txt_centro("ACERTOU?", y_card + 200, font_grande, COR_BOTAO_BASE)
    
    # Usamos a fonte de emoji aqui
    txt_centro("Deixe nos comentários! 👇", y_card + 400, font_media_emoji, 'black')
    txt_centro("❤️ Curta e Siga para mais", y_card + 520, font_media_emoji, (100, 100, 100))
    
    clip_textos = ImageClip(np.array(img)).with_duration(duracao_final)
    clip_final_visual = CompositeVideoClip([fundo, clip_textos]).with_duration(duracao_final)
    
    if audio_encerramento:
        clip_final_visual = clip_final_visual.with_audio(audio_encerramento)
        
    return clip_final_visual

# --- LÓGICA DE VÍDEO ---
def criar_clip_pergunta(dados_pergunta, numero, clip_fundo_base):
    if "audio_path" not in dados_pergunta: return None

    audio_voz = AudioFileClip(dados_pergunta["audio_path"])
    tempo_leitura = audio_voz.duration
    tempo_pensar, tempo_resposta = 5.0, 2.0
    duracao_total = tempo_leitura + tempo_pensar + tempo_resposta

    fundo = clip_fundo_base.with_duration(duracao_total)
    clip_card = criar_card_pergunta_integrado(dados_pergunta['pergunta']).with_duration(duracao_total)

    clips_botoes = []
    for i, opcao in enumerate(dados_pergunta['opcoes']):
        eh_correta = (i == dados_pergunta['correta'])
        letra = ['A', 'B', 'C'][i]
        
        btn_normal = criar_botao_pillow(opcao, letra, COR_BOTAO_BASE, 850 + (i*260)).with_duration(tempo_leitura + tempo_pensar)
        cor_final = COR_BOTAO_CERTO if eh_correta else COR_BOTAO_BASE
        btn_final = criar_botao_pillow(opcao, letra, cor_final, 850 + (i*260)).with_start(tempo_leitura + tempo_pensar).with_duration(tempo_resposta)

        if eh_correta: btn_final = btn_final.resized(lambda t: 1.0 + 0.05 * np.sin(t * 10)) 

        clips_botoes.extend([btn_normal, btn_final])

    clips_timer = [criar_timer_pillow(t).with_start(tempo_leitura + (5 - t)).with_duration(1) for t in range(5, 0, -1)]

    audios = [audio_voz]
    if os.path.exists(SOM_TIC_TAC):
        try:
            tic_tac_base = AudioFileClip(SOM_TIC_TAC).with_volume_scaled(0.5)
            audios.append(concatenate_audioclips([tic_tac_base] * (int(tempo_pensar / tic_tac_base.duration) + 2)).subclipped(0, tempo_pensar).with_start(tempo_leitura))
        except: pass

    if os.path.exists(SOM_CORRETO):
        try: audios.append(AudioFileClip(SOM_CORRETO).with_start(tempo_leitura + tempo_pensar))
        except: pass

    return CompositeVideoClip([fundo, clip_card] + clips_botoes + clips_timer).with_audio(CompositeAudioClip(audios)).with_duration(duracao_total)

def gerar_video_final(quiz_data, nome_arquivo="quiz_pronto.mp4", video_fundo_path="assets/background_minecraft.mp4"):
    print(f"\n--- 🎬 Renderizando (Fundo: {video_fundo_path}) ---")
    
    clip_bg = None
    if os.path.exists(video_fundo_path):
        try:
            bg = VideoFileClip(video_fundo_path).without_audio()
            # Loop infinito (repete 50x)
            bg = concatenate_videoclips([bg] * 50)
            clip_bg = bg.resized(height=ALTURA).cropped(x1=bg.resized(height=ALTURA).w/2 - LARGURA/2, width=LARGURA, height=ALTURA)
        except Exception as e: 
            print(f"⚠️ Erro ao carregar fundo: {e}")
            pass
            
    if clip_bg is None: clip_bg = ColorClip(size=(LARGURA, ALTURA), color=(30, 30, 30))

    clips_finais = []
    tempo_acumulado = 0
    
    for i, item in enumerate(quiz_data):
        print(f"🔨 Q{i+1}: Desenhando...")
        bg_da_vez = clip_bg
        if isinstance(clip_bg, VideoFileClip) and clip_bg.duration:
            bg_da_vez = clip_bg.subclipped(tempo_acumulado % clip_bg.duration, clip_bg.duration)
            
        clip = criar_clip_pergunta(item, i+1, bg_da_vez)
        if clip:
            clips_finais.append(clip)
            tempo_acumulado += clip.duration

    if clips_finais:
        print("🎬 Adicionando Tela Final...")
        bg_da_vez = clip_bg
        if isinstance(clip_bg, VideoFileClip) and clip_bg.duration:
            bg_da_vez = clip_bg.subclipped(tempo_acumulado % clip_bg.duration, clip_bg.duration)
        clips_finais.append(criar_clip_encerramento(bg_da_vez))

    if not clips_finais: return

    print("🚀 Concatenando vídeo base...")
    final = concatenate_videoclips(clips_finais, method="compose")
    
    if os.path.exists(SOM_FUNDO):
        print("🎵 Adicionando Trilha Sonora...")
        try:
            musica = AudioFileClip(SOM_FUNDO).with_volume_scaled(0.15)
            musica_longa = concatenate_audioclips([musica] * (int(final.duration / musica.duration) + 1))
            audio_final_mixado = CompositeAudioClip([final.audio, musica_longa.subclipped(0, final.duration)])
            final = final.with_audio(audio_final_mixado)
        except Exception as e:
            print(f"⚠️ Erro música: {e}")

    pasta_destino = os.path.join("assets", "videos_prontos")
    os.makedirs(pasta_destino, exist_ok=True)
    
    caminho = os.path.join(pasta_destino, nome_arquivo)
    
    final.write_videofile(caminho, fps=24, codec='libx264', audio_codec='aac', preset='medium') 
    print(f"✅ VÍDEO PRONTO: {caminho}")

if __name__ == "__main__":
    pass