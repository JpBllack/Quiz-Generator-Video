import json
import os

def carregar_quiz():
    """
    Lê o arquivo 'quiz.json' e retorna a lista de perguntas.
    """
    caminho_arquivo = "quiz.json"
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Erro: O arquivo '{caminho_arquivo}' não foi encontrado na pasta do projeto.")
        return []

    try:
        # Abre o arquivo com encoding utf-8 para aceitar acentos
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
        print(f"✅ Arquivo carregado! Encontradas {len(dados)} perguntas.")
        return dados

    except json.JSONDecodeError:
        print("❌ Erro: O arquivo quiz.json está com a formatação errada (vírgula ou chave faltando).")
        return []
    except Exception as e:
        print(f"❌ Erro desconhecido: {e}")
        return []

# Teste rápido
if __name__ == "__main__":
    resultado = carregar_quiz()
    print(resultado)