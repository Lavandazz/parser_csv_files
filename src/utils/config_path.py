import os

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.normpath(os.path.join(UTILS_DIR, '..', '..'))  # поднимаемся в базовую папку и строим путь
FOLDER = "data"
DATA_DIR = os.path.join(BASE_DIR, FOLDER)
