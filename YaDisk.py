import requests

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f'OAuth {self.token}'            
        }

    def create_folder(self, path_to_folder):
        URL = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {
            "path": path_to_folder
        }
        response = requests.put(URL, headers=headers, params=params)
        return

    def upload_file_by_link(self, url, path_on_yadisk):
        URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {
            "path": path_on_yadisk,
            "url": url
        }
        response = requests.post(URL, headers=headers, params=params)
        return