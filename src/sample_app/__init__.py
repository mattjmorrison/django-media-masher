from os import path
APP_DIR = path.abspath(path.dirname(__file__))
STATIC_PATH = path.join(APP_DIR, 'media', 'sample_app')
JS_DIR = path.join(STATIC_PATH, 'js')
