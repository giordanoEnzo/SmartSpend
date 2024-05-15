from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def autenticar(self):
        gauth = GoogleAuth()
        gauth.settings['client_config_file'] = None
        gauth.settings['client_id'] = self.client_id
        gauth.settings['client_secret'] = self.client_secret
        gauth.settings['save_credentials'] = True
        gauth.settings['oauth_scope'] = ['https://www.googleapis.com/auth/drive']
        gauth.settings['get_refresh_token'] = True
        gauth.LocalWebserverAuth()
        return gauth

    def upload_arquivo(self, nome_arquivo, caminho_arquivo, pasta_destino_id):
        gauth = self.autenticar()
        drive = GoogleDrive(gauth)
        arquivo = drive.CreateFile({'title': nome_arquivo, 'parents': [{'id': pasta_destino_id}]})
        arquivo.SetContentFile(caminho_arquivo)
        arquivo.Upload()
        print("Upload concluído: ", arquivo['title'])

    def download_arquivo(self, nome_arquivo, caminho_destino):
        gauth = self.autenticar()
        drive = GoogleDrive(gauth)
        arquivo_lista = drive.ListFile({'q': "title='" + nome_arquivo + "' and trashed=false"}).GetList()
        if len(arquivo_lista) == 0:
            print("Arquivo não encontrado.")
            return
        for arquivo in arquivo_lista:
            arquivo.GetContentFile(caminho_destino)
            print("Download concluído: ", arquivo['title'])




