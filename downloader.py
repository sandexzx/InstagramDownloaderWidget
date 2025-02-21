import instaloader
from bs4 import BeautifulSoup
import requests
import json
import re
import os
import shutil
import sys
from datetime import datetime
import ffmpeg
import subprocess

# Настраиваем повторные попытки для всех HTTP запросов
import urllib3
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def modify_metadata(input_file, output_file):
    """Изменяем метаданные видео на текущую дату/время"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Создаём временный файл с измененными метаданными
        temp_output = input_file + "_temp.mp4"
        
        # Формируем команду ffmpeg для изменения метаданных
        cmd = [
            'ffmpeg', '-i', input_file,
            '-metadata', f'creation_time={current_time}',
            '-c', 'copy',  # Копируем видео и аудио без перекодирования
            temp_output
        ]
        
        # Выполняем команду
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Перемещаем временный файл на место финального
        shutil.move(temp_output, output_file)
        
        # Делаем файл доступным для чтения всем
        os.chmod(output_file, 0o644)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error modifying metadata: {str(e)}")
        # Если что-то пошло не так, просто копируем оригинальный файл
        shutil.copy(input_file, output_file)
        os.chmod(output_file, 0o644)
        return False

def download_reel(url):
    # Создаём экземпляр загрузчика с юзер-агентом
    L = instaloader.Instaloader(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False
    )
    
    # Если у тебя есть прокси, можно добавить такую строку:
    # L.context._session.proxies = {'http': 'http://user:pass@proxy:port', 'https': 'https://user:pass@proxy:port'}
    
    # Извлекаем shortcode из URL
    shortcode = url.split("/")[-2]
    
    try:
        # Получаем пост по shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Создаём временную директорию для загрузки
        temp_dir = f"reels_{shortcode}"
        
        # Качаем видео
        L.download_post(post, target=temp_dir)
        
        # Используем директорию Movies для видео
        reels_dir = os.path.expanduser("~/storage/shared/Movies/Instagram")
        
        # Проверяем/создаём директорию
        os.makedirs(reels_dir, exist_ok=True)
        
        # Ищем .mp4 файл и обрабатываем его
        for file in os.listdir(temp_dir):
            if file.endswith(".mp4"):
                input_path = os.path.join(temp_dir, file)
                output_path = os.path.join(reels_dir, f"Reel_{shortcode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
                
                # Модифицируем метаданные
                metadata_success = modify_metadata(input_path, output_path)
                
                # Обновляем медиа сканер
                os.system(f'termux-media-scan {output_path}')
                
                # Отправляем уведомление
                if metadata_success:
                    os.system('termux-notification -t "Reel Downloaded!" -c "Successfully saved to Movies/Instagram"')
                else:
                    os.system('termux-notification -t "Reel Downloaded!" -c "Saved to Movies/Instagram (metadata update failed)"')
                
                break
        
        # Удаляем временную директорию
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        os.system(f'termux-notification -t "Download Failed!" -c "Error: {str(e)}"')
        raise e

def download_reel_alternative(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15.0 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Получаем страницу
        response = http.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Не удалось получить страницу: {response.status_code}")
        
        # Ищем JSON-данные в HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        video_url = None
        
        # Ищем URL видео в скриптах
        for script in scripts:
            if script.string and "video_url" in script.string:
                json_text = re.search(r'window\._sharedData\s*=\s*({.*?});', script.string)
                if json_text:
                    data = json.loads(json_text.group(1))
                    # Тут надо будет покопаться в структуре JSON, чтобы найти video_url
                    # Примерно так:
                    # video_url = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_url']
                    # Но точная структура может отличаться
        
        # Если не нашли в _sharedData, поищем в другом месте
        if not video_url:
            for script in scripts:
                if script.string and '"VideoObject"' in script.string:
                    matches = re.findall(r'"contentUrl":"(https:[^"]+)"', script.string)
                    if matches:
                        video_url = matches[0].replace('\\u0026', '&')
        
        if not video_url:
            raise Exception("Не удалось найти URL видео")
        
        # Получаем shortcode из URL
        shortcode = url.split("/")[-2]
        
        # Создаём директорию для сохранения
        reels_dir = os.path.expanduser("~/storage/shared/Movies/Instagram")
        os.makedirs(reels_dir, exist_ok=True)
        
        # Имя выходного файла
        output_path = os.path.join(reels_dir, f"Reel_{shortcode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        # Скачиваем файл
        video_response = http.get(video_url, headers=headers, stream=True)
        
        if video_response.status_code != 200:
            raise Exception(f"Не удалось скачать видео: {video_response.status_code}")
        
        # Сохраняем во временный файл
        temp_file = f"/tmp/temp_reel_{shortcode}.mp4"
        with open(temp_file, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Модифицируем метаданные и перемещаем
        modify_metadata(temp_file, output_path)
        
        # Обновляем медиа сканер
        os.system(f'termux-media-scan {output_path}')
        
        # Отправляем уведомление
        os.system('termux-notification -t "Reel Downloaded!" -c "Successfully saved to Movies/Instagram"')
        
        # Удаляем временный файл
        os.remove(temp_file)
        return True
        
    except Exception as e:
        os.system(f'termux-notification -t "Download Failed!" -c "Alt Method: {str(e)}"')
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if "instagram.com" in url and "/reel/" in url:
            try:
                download_reel(url)
            except Exception as e:
                print(f"Основной метод не сработал: {str(e)}")
                print("Пробую альтернативный метод...")
                download_reel_alternative(url)
        else:
            os.system('termux-notification -t "Invalid Link" -c "Please copy an Instagram Reel link!"')
    else:
        os.system('termux-notification -t "Error" -c "No URL provided!"')