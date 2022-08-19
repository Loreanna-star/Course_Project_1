import requests

class VKUser:

    def __init__(self, token, version, owner_id):
        self.params = {
            'access_token': token,
            'v': version,
            'owner_id': owner_id  
        }

    def get_photos_info(self, album_id):
        URL = "https://api.vk.com/method/photos.get"
        get_photos_params = {
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 1
        }
        res = requests.get(URL, params={**self.params, **get_photos_params}).json()
        return res