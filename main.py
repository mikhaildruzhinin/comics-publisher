import requests
import os
from pathlib import Path
import random
from dotenv import load_dotenv

def save_pic(url, filepath):
    filename, file_extension = get_filename_and_extension(url)
    filename = f'{filename}{file_extension}'
    response = requests.get(url)
    response.raise_for_status()

    Path(filepath).mkdir(parents=True, exist_ok=True)
    filepath = Path('images') / Path(filename)

    with filepath.open('wb') as file:
        file.write(response.content)
    return filename

def get_filename_and_extension(url):
    filename = url.split('/')[-1]
    filename, file_extension = os.path.splitext(filename)
    return filename, file_extension

def get_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    num = response.json()['num']
    return num

def fetch_xkcd_comic(number):
    url = f'http://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    collected_data = response.json()
    image = collected_data['img']
    filename = save_pic(image, 'images')
    message = collected_data['alt']
    return filename, message

def get_groups_info(access_token, v):
    url = 'https://api.vk.com/method/groups.get'
    payload = {
        'access_token': access_token,
        'v': v,
    }
    response = requests.get(url, params=payload)
    collected_data = response.json()
    if 'error' in collected_data:
        raise requests.exceptions.HTTPError(collected_data['error'])
    return collected_data

def get_group_upload_url(group_id, access_token, v):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': v,
    }
    response = requests.get(url, params=payload)
    collected_data = response.json()
    if 'error' in collected_data:
        raise requests.exceptions.HTTPError(collected_data['error'])
    return collected_data

def upload_pic(filename, upload_url):
    filepath = f'images/{filename}'
    with open(filepath, 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        collected_data = response.json()
        if 'error' in collected_data:
            raise requests.exceptions.HTTPError(collected_data['error'])
        return collected_data['photo'], collected_data['server'], collected_data['hash']

def save_pic_in_group(group_id, photo, server, hash_, access_token, v):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash_,
        'access_token': access_token,
        'v': v,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    collected_data = response.json()
    if 'error' in collected_data:
        raise requests.exceptions.HTTPError(collected_data['error'])
    return collected_data['response'][0]['id'], collected_data['response'][0]['owner_id']

def post_pic(group_id, owner_id, media_id, message, access_token, v):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': message,
        'access_token': access_token,
        'v': v,
    }
    response = requests.post(url, params=payload)
    collected_data = response.json()
    if 'error' in collected_data:
        raise requests.exceptions.HTTPError(collected_data['error'])
    return collected_data

def delete_file(filename):
    filepath = f'images/{filename}'
    if os.path.isfile(filepath):
        os.remove(filepath)

def main():
    total_number = get_comic_number()
    comic_number = random.randint(1, total_number)
    filename, message = fetch_xkcd_comic(comic_number)
    
    load_dotenv()
    access_token = os.getenv('VK_ACCESS_TOKEN')
    v = 5.103
    group_id = os.getenv('VK_GROUP_ID')

    try:
        upload_url = get_group_upload_url(group_id, access_token, v)['response']['upload_url']
        photo, server, hash_ = upload_pic(filename, upload_url)
        media_id, owner_id = save_pic_in_group(group_id, photo, server, hash_, access_token, v)
        res = post_pic(group_id, owner_id, media_id, message, access_token, v)
    finally:
        delete_file(filename)

if __name__=='__main__':
    main()
