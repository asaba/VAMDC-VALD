import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.oacagliari.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
path = '/var/www/wsgi/VAMDC/'
if path not in sys.path:
    sys.path.append(path)
