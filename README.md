# 📱 Instagram Reels Downloader для Termux

Простой, но мощный скрипт для скачивания Instagram Reels прямо на ваш Android-смартфон через Termux. Никаких заморочек - просто копируете ссылку на рилс и готово! 🚀

## 🔥 Фишки

- Скачивание Instagram Reels в один клик
- Автоматическое сохранение в папку Movies/Instagram
- Push-уведомления о статусе загрузки
- Сохранение актуальных метаданных видео
- Виджет для быстрого доступа с главного экрана
- Не требует логина в Instagram

## 📱 Требования

- Android смартфон
- Установленный [Termux](https://f-droid.org/packages/com.termux/)
- Установленный [Termux:API](https://f-droid.org/packages/com.termux.api/)
- Разрешение на доступ к хранилищу для Termux

## 🛠️ Установка

1. Откройте Termux и вставьте следующую команду:

```bash
curl -s https://raw.githubusercontent.com/sandexzx/InstagramDownloaderWidget/main/SetupDownloader.sh | bash
```

2. Дождитесь завершения установки. Скрипт автоматически:
   - Установит все необходимые зависимости
   - Создаст нужные директории
   - Настроит скрипты
   - Сделает их исполняемыми

## 💫 Как использовать

### Через виджет (рекомендуется):
1. Скопируйте ссылку на понравившийся рилс
2. Нажмите на виджет "Download Reel" на главном экране
3. Готово! Видео появится в папке Movies/Instagram

### Через терминал:
```bash
~/.shortcuts/download_reel
```

## 📂 Структура файлов

```
└── $HOME
    ├── scripts/
    │   └── download_reel.py    # Основной скрипт загрузки
    ├── .shortcuts/
    │   └── download_reel       # Скрипт-шорткат для виджета
    └── storage/shared/Movies/Instagram/
        └── ...                 # Загруженные видео
```

## 🔧 Технические детали

Скрипт использует:
- `instaloader` для загрузки контента
- `ffmpeg` для работы с метаданными
- `termux-api` для уведомлений и доступа к буферу обмена

## ⚠️ Важно

- Скрипт работает только с публичными рилсами
- Используйте ответственно и уважайте авторские права
- Загруженный контент предназначен только для личного использования

## 🐛 Решение проблем

1. **Ошибка "Invalid Link"**
   - Убедитесь, что ссылка начинается с "instagram.com" и содержит "/reel/"
   
2. **Ошибка "No URL provided"**
   - Проверьте, что ссылка скопирована в буфер обмена

3. **Нет доступа к хранилищу**
   ```bash
   termux-setup-storage
   ```

## 📝 Лицензия

Делайте что хотите, just give credit 😉

## 🤝 Вклад в проект

Баги нашли? Есть идеи по улучшению? Welcome:
1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Пушните в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Связь

- Создайте Issue в этом репозитории
- Напишите мне в [Telegram](https://t.me/VRN_Aleksandr_Zverev)




# 📱 Instagram Reels Downloader for Termux

A lightweight yet powerful script for downloading Instagram Reels directly to your Android smartphone via Termux. No complications - just copy the reel link and you're good to go! 🚀

## 🔥 Features

- One-click Instagram Reels downloading
- Automatic saving to Movies/Instagram folder
- Push notifications for download status
- Up-to-date video metadata preservation
- Home screen widget for quick access
- No Instagram login required

## 📱 Requirements

- Android smartphone
- [Termux](https://f-droid.org/packages/com.termux/) installed
- [Termux:API](https://f-droid.org/packages/com.termux.api/) installed
- Storage permission granted for Termux

## 🛠️ Installation

1. Open Termux and paste the following command:

```bash
curl -s https://raw.githubusercontent.com/sandexzx/InstagramDownloaderWidget/main/SetupDownloader.sh | bash
```

2. Wait for the installation to complete. The script will automatically:
   - Install all necessary dependencies
   - Create required directories
   - Set up scripts
   - Make them executable

## 💫 How to Use

### Via Widget (Recommended):
1. Copy the link of the reel you want to download
2. Tap the "Download Reel" widget on your home screen
3. Done! The video will appear in the Movies/Instagram folder

### Via Terminal:
```bash
~/.shortcuts/download_reel
```

## 📂 File Structure

```
└── $HOME
    ├── scripts/
    │   └── download_reel.py    # Main download script
    ├── .shortcuts/
    │   └── download_reel       # Widget shortcut script
    └── storage/shared/Movies/Instagram/
        └── ...                 # Downloaded videos
```

## 🔧 Technical Details

The script utilizes:
- `instaloader` for content downloading
- `ffmpeg` for metadata manipulation
- `termux-api` for notifications and clipboard access

## ⚠️ Important Notes

- Script works only with public reels
- Use responsibly and respect copyright
- Downloaded content is for personal use only

## 🐛 Troubleshooting

1. **"Invalid Link" Error**
   - Ensure the link starts with "instagram.com" and contains "/reel/"
   
2. **"No URL provided" Error**
   - Verify that the link is copied to clipboard

3. **Storage Access Issues**
   ```bash
   termux-setup-storage
   ```

## 📝 License

Do whatever you want, just give credit 😉

## 🤝 Contributing

Found bugs? Have ideas for improvements? You're welcome to contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

- Create an Issue in this repository
- Reach out via [Telegram](https://t.me/VRN_Aleksandr_Zverev)

## ⚙️ Dependencies

The script requires the following Python packages:
- instaloader
- beautifulsoup4
- requests
- ffmpeg-python

And the following Termux packages:
- python
- termux-api
- ffmpeg

## 🔍 How It Works

The script performs the following operations:
1. Extracts the reel's shortcode from the URL
2. Downloads the video using instaloader
3. Updates the video metadata to current date/time
4. Moves the file to the Movies/Instagram directory
5. Sends a notification about the download status
6. Cleans up temporary files

## 🆘 Common Issues and Solutions

1. **Download fails immediately**
   - Check your internet connection
   - Verify that the reel is from a public account
   - Ensure Termux has storage permissions

2. **Widget doesn't appear**
   - Reinstall Termux:Widget
   - Ensure the shortcut script is properly placed in ~/.shortcuts

3. **Video doesn't appear in gallery**
   - Try running `termux-media-scan` manually
   - Check if the Movies/Instagram directory exists
   - Verify storage permissions

## 📱 Compatibility

- Works on Android 7.0 and above
- Tested on various Android distributions
- Compatible with most modern Android file managers
