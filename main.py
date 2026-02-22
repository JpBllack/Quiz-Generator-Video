import os
from quiz_generator import carregar_quiz
from voice_generator import processar_vozes_do_quiz
from video_generator import gerar_video_final

def gerar_nome_sequencial(categoria):
    """
    Entra na pasta, conta quantos vídeos da categoria existem e gera o próximo.
    Ex: Se já tem cristao_1.mp4 e cristao_2.mp4, ele retorna cristao_3.mp4
    """
    pasta_destino = os.path.join("assets", "videos_prontos")
    os.makedirs(pasta_destino, exist_ok=True) # Garante que a pasta existe
    
    # Lista todos os arquivos na pasta que começam com o nome da categoria
    arquivos_existentes = [f for f in os.listdir(pasta_destino) if f.startswith(categoria) and f.endswith(".mp4")]
    
    # O próximo número é a quantidade de arquivos que já existem + 1
    proximo_numero = len(arquivos_existentes) + 1
    
    return f"{categoria}_{proximo_numero}.mp4"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=============================================")
    print("🎬 FABRICA DE VÍDEOS (MODO JSON MANUAL)")
    print("=============================================")
    print("Certifique-se que você salvou o roteiro em 'quiz.json'\n")

    # 1. Carrega o arquivo
    quiz_data = carregar_quiz()
    if not quiz_data:
        return 

    # 2. Gera Vozes
    print("\n🎤 Processando áudios...")
    try:
        quiz_com_audio = processar_vozes_do_quiz(quiz_data)
    except Exception as e:
        print(f"❌ Erro no áudio: {e}")
        return

    # 3. ESCOLHA DO FUNDO E CATEGORIA
    print("\n🖼️ Escolha o TEMA do vídeo de fundo:")
    print(" [ 1 ] - Cristão / Teologia")
    print(" [ 2 ] - Musculação / Fitness")
    print(" [ 3 ] - Música / Instrumentos")
    print(" [ 4 ] - Aleatório (Minecraft)")
    
    escolha = input("Digite a opção (1/2/3/4) [Padrão: 4]: ").strip()
    
    if escolha == '1':
        caminho_fundo = os.path.join("assets", "background_cristao.mp4")
        categoria = "cristao"
        print("🙏 Fundo selecionado: Cristão")
    elif escolha == '2':
        caminho_fundo = os.path.join("assets", "background_musculacao.mp4")
        categoria = "musculacao"
        print("💪 Fundo selecionado: Musculação")
    elif escolha == '3':
        caminho_fundo = os.path.join("assets", "background_musica.mp4")
        categoria = "musica"
        print("🎸 Fundo selecionado: Música")
    else:
        caminho_fundo = os.path.join("assets", "background_minecraft.mp4")
        categoria = "aleatorio"
        print("⛏️ Fundo selecionado: Minecraft (Aleatório)")

    # 4. GERA O NOME DO ARQUIVO SEQUENCIAL (A Mágica!)
    nome_video = gerar_nome_sequencial(categoria)
    print(f"\n📝 Nome do arquivo será: {nome_video}")

    # 5. Gera Vídeo
    gerar_video_final(quiz_com_audio, nome_video, caminho_fundo)

    print(f"\n✨ PRONTO! Vídeo salvo na sua galeria: assets/videos_prontos/{nome_video}")

if __name__ == "__main__":
    main()