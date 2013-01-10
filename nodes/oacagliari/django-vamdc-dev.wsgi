import os
import sys
sys.path.append('/var/www/wsgi/VAMDC')


os.environ['DJANGO_SETTINGS_MODULE'] = 'nodes.oacagliari.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

