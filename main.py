import os
import json
from gui import run_app

if __name__ == "__main__":
    # Загружаем историю из файла или создаем пустую
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    run_app(history)
