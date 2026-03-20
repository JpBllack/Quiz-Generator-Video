import os
import random
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

def gerar_video_vendas(caminho_audio, nome_saida, pasta_broll, cenas):
    print(f"🎬 Iniciando renderização de VENDAS: {nome_saida}")
    
    # 1. Carrega o áudio e descobre o tempo total
    audio = AudioFileClip(caminho_audio)
    duracao_total = audio.duration
    
    # 2. Busca os vídeos de fundo (B-Roll)
    caminho_pasta_broll = os.path.join("assets", "b_roll", pasta_broll)
    if not os.path.exists(caminho_pasta_broll):
        os.makedirs(caminho_pasta_broll)
        
    arquivos_broll = [os.path.join(caminho_pasta_broll, f) for f in os.listdir(caminho_pasta_broll) if f.endswith('.mp4')]
    
    if not arquivos_broll:
        raise Exception(f"❌ Nenhum vídeo encontrado! Coloque alguns MP4 na pasta: {caminho_pasta_broll}")
        
    random.shuffle(arquivos_broll) # Mistura os takes pra não ficar repetitivo
    
    # 3. Junta os vídeos até cobrir o tempo todo do áudio da narração
    clipes_fundo = []
    tempo_acumulado = 0
    
    while tempo_acumulado < duracao_total:
        for video_path in arquivos_broll:
            clip = VideoFileClip(video_path)
            
            # Redimensiona para formato Shorts (1080x1920) cortando as laterais automaticamente
            if clip.w > clip.h:
                clip = clip.resize(height=1920)
                clip = clip.crop(x_center=clip.w/2, width=1080)
            else:
                clip = clip.resize(width=1080, height=1920)
                
            clipes_fundo.append(clip)
            tempo_acumulado += clip.duration
            if tempo_acumulado >= duracao_total:
                break
                
    video_fundo = concatenate_videoclips(clipes_fundo).subclip(0, duracao_total)
    
    # 4. Cria as Legendas Gigantes no meio da tela
    textos_clips = []
    tempo_atual = 0
    
    for cena in cenas:
        texto = cena.get("texto", "")
        tempo_cena = cena.get("tempo", 3)
        
        if tempo_atual >= duracao_total:
            break
        if tempo_atual + tempo_cena > duracao_total:
            tempo_cena = duracao_total - tempo_atual
            
        txt_clip = TextClip(
            texto, 
            fontsize=85, 
            color='yellow', 
            font='Impact', 
            method='caption', 
            size=(900, None), # Margem de segurança pro texto não sair da tela
            stroke_color='black',
            stroke_width=4
        )
        
        # Centraliza o texto e define a hora que ele aparece e some
        txt_clip = txt_clip.set_position('center').set_start(tempo_atual).set_duration(tempo_cena)
        textos_clips.append(txt_clip)
        tempo_atual += tempo_cena
        
    # 5. O Grande Final: Fundo + Legendas + Áudio
    video_final = CompositeVideoClip([video_fundo] + textos_clips)
    video_final = video_final.set_audio(audio)
    
    # 6. Renderiza pro disco
    caminho_final = os.path.join("assets", "videos_prontos", nome_saida)
    video_final.write_videofile(
        caminho_final, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac",
        threads=4,
        preset="ultrafast"
    )
    
    print(f"✅ VÍDEO DE VENDAS PRONTO: {caminho_final}")
    return caminho_final