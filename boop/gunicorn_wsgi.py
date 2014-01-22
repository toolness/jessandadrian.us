import subprocess
import sys
from dj_static import Cling

from .wsgi import application

# Heroku is supposed to do this for us, but it's not, so we'll
# do it ourselves at startup.
#
# Also don't crash if this fails, as gunicorn/Heroku will just
# keep infinitely restarting the process.
subprocess.Popen([
  sys.executable, 'manage.py', 'collectstatic', '--noinput'
]).wait()

application = Cling(application)
