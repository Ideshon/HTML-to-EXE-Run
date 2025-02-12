# -*- coding: utf-8 -*-

import os
import random
import webbrowser
import yaml
from http.server import HTTPServer, SimpleHTTPRequestHandler

#try:
#    import pyi_splash
#    pyi_splash.close()  # Если PyInstaller формирует splash-окно, закроем его
#except:
#    pass

# Базовые настройки
settings = {
    "random-port": False,
    "random-port-range": [8000, 65535],
    "file-to-load": "test.htm"
}

config_path = "config.yml"
default_html = "test.htm"

# Проверяем, существует ли config.yml
if os.path.isfile(config_path):
    # Читаем YAML с указанием кодировки и разрешением unicode
    with open(config_path, "r", encoding="utf-8") as f:
        temp = yaml.safe_load(f)

    # Объединяем настройки, чтобы не потерять новые ключи
    for key in settings:
        if key not in temp:
            temp[key] = settings[key]

    # Перезаписываем config.yml (сохраняем unicode)
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(temp, f, allow_unicode=True)

    # Обновлённые настройки
    settings = temp
else:
    # Если config.yml нет, создаём с настройками по умолчанию
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(settings, f, allow_unicode=True)

# Если нет test.htm и в настройках "file-to-load" тоже test.htm — создаём простой HTML
if not os.path.isfile(default_html) and settings["file-to-load"] == default_html:
    with open(default_html, "w", encoding="utf-8") as f:
        f.write("<html><body>Hey dummy!</body></html>")

# Определяем порт для запуска сервера
if settings["random-port"]:
    port = random.randint(settings["random-port-range"][0], settings["random-port-range"][1])
else:
    port = 8000

# Запускаем простой HTTP-сервер
httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)

# Открываем в браузере страницу, указанную в настройках
# Если там будет имя файла с русскими буквами, Python 3 корректно обработает Unicode в пути
webbrowser.open(f"http://localhost:{port}/{settings['file-to-load']}")

# Запускаем сервер (блокирует выполнение, пока не прервём)
httpd.serve_forever()
