from quiz_generator import carregar_quiz
from voice_generator import processar_vozes_do_quiz
from video_generator import gerar_video_final # <--- Import novo

def main():
    print("--- 🎬 Gerador de Quiz (Completo) ---")
    
    # 1. Carregar (JSON)
    quiz_data = carregar_quiz()
    if not quiz_data: return

    # 2. Voz (ElevenLabs)
    quiz_com_audio = processar_vozes_do_quiz(quiz_data)

    # 3. Vídeo (MoviePy)
    gerar_video_final(quiz_com_audio, "quiz_tiktok_v1.mp4")

if __name__ == "__main__":
    main()