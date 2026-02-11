"""
Скрипт сборки Windows-приложения RateShop.

Инструкция:
1. Сначала соберите фронтенд:
   cd frontend && npm install && npm run build

2. Установите зависимости бэкенда:
   cd backend && pip install -r requirements.txt

3. Установите PyInstaller:
   pip install pyinstaller

4. Запустите этот скрипт:
   python build_win.py

Результат: папка dist/RateShop/ с файлом RateShop.exe
При запуске .exe открывается браузер на http://localhost:8000
"""

import os
import subprocess
import sys


def build():
    root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root, "backend")
    frontend_dist = os.path.join(root, "frontend", "dist")

    if not os.path.exists(frontend_dist):
        print("ОШИБКА: Папка frontend/dist не найдена!")
        print("Сначала соберите фронтенд: cd frontend && npm run build")
        sys.exit(1)

    # Create launcher script
    launcher = os.path.join(root, "rateshop_launcher.py")
    with open(launcher, "w", encoding="utf-8") as f:
        f.write('''
import os
import sys
import webbrowser
import threading
import time

# Set paths
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add backend to path
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
os.chdir(os.path.join(BASE_DIR, "backend"))

# Import and setup
from database import init_db, DB_PATH
from seed_data import seed

# Override DB path for portable use
import database
if getattr(sys, 'frozen', False):
    database.DB_PATH = os.path.join(os.path.dirname(sys.executable), "rateshop.db")

init_db()
seed()

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")

threading.Thread(target=open_browser, daemon=True).start()

import uvicorn
from main import app
uvicorn.run(app, host="127.0.0.1", port=8000)
''')

    print("Запуск PyInstaller...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=RateShop",
        "--onedir",
        "--windowed",
        f"--add-data={backend_dir}{os.pathsep}backend",
        f"--add-data={frontend_dist}{os.pathsep}frontend/dist",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.lifespan.off",
        "--collect-all=fastapi",
        "--collect-all=starlette",
        launcher,
    ]

    subprocess.run(cmd, check=True)
    print("\n✅ Сборка завершена! Файл: dist/RateShop/RateShop.exe")


if __name__ == "__main__":
    build()
