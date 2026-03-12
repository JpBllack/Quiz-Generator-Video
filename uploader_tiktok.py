import os
from tiktok_uploader.upload import upload_video

def fazer_upload_tiktok(caminho_video, descricao):
    print(f"🎵 Preparando upload para o TikTok: {caminho_video}")
    
    caminho_cookies = "cookies.txt"
    
    if not os.path.exists(caminho_cookies):
        print("❌ ERRO: Arquivo cookies.txt não encontrado na pasta!")
        return False
        
    try:
        # A biblioteca abre um navegador invisível, injeta seus cookies e faz o post
        upload_video(
            filename=caminho_video,
            description=descricao,
            cookies=caminho_cookies
        )
        print("✅ Upload no TikTok concluído com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao postar no TikTok: {e}")
        return False