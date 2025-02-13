#!/bin/bash

# Функция для проверки доступа к storage
check_storage_access() {
    if [ ! -d ~/storage/shared ]; then
        echo "🔄 Storage access not configured. Setting up..."
        termux-setup-storage
        
        # Ждём пока пользователь подтвердит разрешение
        for i in {1..30}; do
            if [ -d ~/storage/shared ]; then
                echo "✅ Storage access granted!"
                return 0
            fi
            echo "⏳ Waiting for storage permission... ($i/30)"
            sleep 1
        done
        
        echo "❌ Storage setup failed! Please run 'termux-setup-storage' manually and grant permission"
        exit 1
    else
        echo "✅ Storage access already configured!"
    fi
}

# Проверяем storage перед началом установки
echo "🔍 Checking storage access..."
check_storage_access

# Проверяем/устанавливаем необходимые пакеты
echo "📦 Installing required packages..."
pkg update -y
pkg install -y python termux-api ffmpeg

# Устанавливаем питоновские библиотеки
echo "🐍 Installing Python libraries..."
pip install instaloader beautifulsoup4 requests ffmpeg-python

# Создаём необходимые директории
echo "📁 Creating directories..."
mkdir -p ~/.shortcuts
mkdir -p ~/scripts
mkdir -p ~/storage/shared/Movies/Instagram

# Создаём Python скрипт для скачивания
echo "📝 Creating download script..."
cat > ~/scripts/download_reel.py << 'EOL'
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
    # Создаём экземпляр загрузчика
    L = instaloader.Instaloader()
    
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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if "instagram.com" in url and "/reel/" in url:
            download_reel(url)
        else:
            os.system('termux-notification -t "Invalid Link" -c "Please copy an Instagram Reel link!"')
    else:
        os.system('termux-notification -t "Error" -c "No URL provided!"')
EOL

# Создаём скрипт-шорткат
echo "🔗 Creating shortcut script..."
cat > ~/.shortcuts/download_reel << 'EOL'
#!/bin/bash

# Получаем ссылку из буфера обмена
URL=$(termux-clipboard-get)

# Запускаем Python скрипт с ссылкой в качестве аргумента
python ~/scripts/download_reel.py "$URL"
EOL

# Делаем скрипты исполняемыми
echo "🔧 Setting permissions..."
chmod +x ~/.shortcuts/download_reel
chmod +x ~/scripts/download_reel.py

echo "✨ Setup completed! 🚀"
echo "Now you can add the Download Reel widget to your home screen!"