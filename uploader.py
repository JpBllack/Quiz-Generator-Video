import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Permissão necessária para fazer upload no YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def obter_servico_youtube():
    creds = None
    # O ficheiro token.pickle armazena a sessão do utilizador para não pedir login sempre
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Se não houver credenciais válidas, abre o ecrã de login do Google
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            # Isto vai abrir o navegador para você permitir o acesso ao seu canal
            creds = flow.run_local_server(port=0)
        
        # Guarda as credenciais no ficheiro para a próxima execução automática
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def fazer_upload_youtube(caminho_video, titulo, descricao, tags):
    youtube = obter_servico_youtube()

    print(f"A preparar o upload de: {titulo}")

    # Configurações do Vídeo
    corpo = {
        'snippet': {
            'title': titulo,
            'description': descricao,
            'tags': tags,
            'categoryId': '24' # 24 = Entretenimento, 27 = Educação
        },
        'status': {
            # ⚠️ IMPORTANTE: Mantemos como 'private' para testar. 
            # Mude para 'public' quando tiver a certeza de que a linha de montagem está perfeita.
            'privacyStatus': 'public', 
            'selfDeclaredMadeForKids': False
        }
    }

    # Carrega o ficheiro de vídeo gerado
    media = MediaFileUpload(caminho_video, chunksize=-1, resumable=True, mimetype='video/mp4')

    request = youtube.videos().insert(
        part=','.join(corpo.keys()),
        body=corpo,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progresso do upload: {int(status.progress() * 100)}%")
    
    print(f"Upload concluído! ID do vídeo: {response.get('id')}")
    return response.get('id')