"""
WSGI config for boop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import subprocess
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boop.settings")

if 'AUTO_COLLECTSTATIC' in os.environ:
    subprocess.Popen([
        sys.executable, 'manage.py', 'collectstatic', '--noinput'
    ], cwd=os.path.dirname(os.path.dirname(__file__))).wait()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from dj_static import Cling
application = Cling(application)
