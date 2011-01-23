from os import path
from masher import site

APP_DIR = path.abspath(path.dirname(__file__))
STATIC_PATH = path.join(APP_DIR, 'media', 'sample_app')
JS_DIR = path.join(STATIC_PATH, 'js')
CSS_DIR = path.join(STATIC_PATH, 'css')

SCRIPT_ONE = site.mash(['%s/one.js' % JS_DIR,
                       '%s/two.js' % JS_DIR,
                       '%s/three.js' % JS_DIR])

STYLE_ONE = site.mash(['%s/one.css' % CSS_DIR,
                       '%s/two.css' % CSS_DIR,
                       '%s/three.css' % CSS_DIR])