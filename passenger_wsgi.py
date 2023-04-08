# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/c/chhhhhz9/chhhhhz9.beget.tech/vchvideo')
sys.path.insert(1, '/home/c/chhhhhz9/chhhhhz9.beget.tech/venv_django/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'vchvideo.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

