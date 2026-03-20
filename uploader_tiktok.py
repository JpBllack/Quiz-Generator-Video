import os
import threading
from tiktok_uploader.upload import upload_video
import playwright.sync_api

# ==========================================
# 🛡️ O EXTERMINADOR DE TUTORIAL (V4 - O Chokepoint Absoluto)
# ==========================================
original_goto = playwright.sync_api.Page.goto

def goto_chokepoint(self, *args, **kwargs):
    # Injeta o script destrutivo na "alma" da página ANTES dela carregar o site
    try:
        self.context.add_init_script("""
            // Roda a cada meio segundo caçando e destruindo o tutorial
            setInterval(() => {
                // Tenta clicar pro TikTok salvar que você já viu (Atualiza o servidor deles)
                document.querySelectorAll('button').forEach(btn => {
                    const txt = (btn.innerText || '').toLowerCase();
                    if (txt.includes('got it') || txt.includes('entendi') || txt.includes('ok')) {
                        btn.click();
                    }
                });
                
                // Destrói a barreira invisível na força bruta para liberar o mouse do robô
                const portal = document.getElementById('react-joyride-portal');
                if (portal) portal.remove();
                
                const overlay = document.querySelector('.react-joyride__overlay');
                if (overlay) overlay.remove();
            }, 500);
            
            // Adiciona o CSS de invisibilidade no topo do HTML por garantia
            window.addEventListener('DOMContentLoaded', () => {
                const style = document.createElement('style');
                style.innerHTML = `
                    #react-joyride-portal, 
                    .react-joyride__overlay, 
                    [data-test-id="overlay"] { 
                        display: none !important; 
                        pointer-events: none !important; 
                        z-index: -9999 !important;
                    }
                `;
                document.documentElement.appendChild(style);
            });
        """)
    except Exception as e:
        print("Aviso: Falha ao injetar vacina:", e)
        
    # Agora sim, manda o robô acessar o TikTok com a página já "envenenada" contra o tutorial
    return original_goto(self, *args, **kwargs)

# Aplica a interceptação final
playwright.sync_api.Page.goto = goto_chokepoint
# ==========================================


def _postar_em_background(caminho_video, descricao, caminho_cookies, resultado):
    try:
        upload_video(
            filename=caminho_video,
            description=descricao,
            cookies=caminho_cookies
        )
        resultado["sucesso"] = True
    except Exception as e:
        resultado["erro"] = str(e)
        resultado["sucesso"] = False

def fazer_upload_tiktok(caminho_video, descricao):
    print(f"🎵 Preparando upload para o TikTok: {caminho_video}")
    
    caminho_cookies = "cookies.txt"
    if not os.path.exists(caminho_cookies):
        print("❌ ERRO: Arquivo cookies.txt não encontrado na pasta!")
        return False
        
    resultado = {"sucesso": False, "erro": None}
    
    thread_tiktok = threading.Thread(
        target=_postar_em_background, 
        args=(caminho_video, descricao, caminho_cookies, resultado)
    )
    thread_tiktok.start() 
    thread_tiktok.join()  
    
    if resultado["sucesso"]:
        print("✅ Upload no TikTok concluído com sucesso (sem travar)!")
        return True
    else:
        print(f"❌ Erro ao postar no TikTok: {resultado['erro']}")
        return False