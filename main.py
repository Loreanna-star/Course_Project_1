import configparser
import json

import pyprind

from VK import VKUser
from YaDisk import YandexDisk


def get_dict_of_links_and_names(all_pictures_info_json):
    types_dict = {"s": 1, "m": 2, "x": 3, "o": 4, "p": 5, "q": 6, "r": 7, "y": 8, "z": 9, "w": 10}  
    dict_of_links_and_names = {}
    for photo in all_pictures_info_json["response"]["items"]:
        grade = 0
        type = ""
        url = ""
        likes = str(photo["likes"]["count"])
        date = photo["date"]
        for size in photo["sizes"]:
            if grade <  types_dict[size["type"]]:
                grade = types_dict[size["type"]]              
                type = size["type"]
                url = size["url"]
                id = photo["id"]        
        if likes not in dict_of_links_and_names.keys():
            name = likes        
        elif f'{likes}_{date}' not in dict_of_links_and_names.keys():
            name = f'{likes}_{date}'
        else:
            name = f'{likes}_{date}_{id}'
        dict_of_links_and_names[name] = {}
        dict_of_links_and_names[name]["url"] = url
        dict_of_links_and_names[name]["type"] = type
    return dict_of_links_and_names

def upload_photos_from_VK_to_YaDisk(VKUser_ID, path_to_folder, album_id, n=5):

    config = configparser.ConfigParser()
    config.read("tokens.ini")
    TOKEN_YADISK = config["YandexDisk"]["TOKEN"]
    TOKEN_VK = config["VK"]["TOKEN"]      
    VERSION = config["VK"]["VERSION"]

    UserVK = VKUser(TOKEN_VK, VERSION, VKUser_ID)     
    YaDiskUser = YandexDisk(TOKEN_YADISK)

    YaDiskUser.create_folder(path_to_folder)
    json_info = UserVK.get_photos_info(album_id)
    json_short_dict = get_dict_of_links_and_names(json_info)
    
    if n > len(json_short_dict):
        i = len(json_short_dict)
    else:
        i = n
    bar = pyprind.ProgBar(i, width=200)

    list_of_files = []
    counter = 0
    for filename, info in json_short_dict.items():      
        url = info["url"]
        path_on_yadisk = f'{path_to_folder}/{filename}'
        YaDiskUser.upload_file_by_link(url, path_on_yadisk)
        list_of_files.append({"filename": filename, "size": info["type"]})
        counter += 1
        bar.update()    
        if counter == n:
            break
        
    with open("logs.json", "w") as f:
        json.dump(list_of_files, f, indent=4)
    return

if __name__ == '__main__':
    upload_photos_from_VK_to_YaDisk("1", "testfolder", "profile", n=10)