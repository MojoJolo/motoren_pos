CSRF_ENABLED = True
SECRET_KEY = 'parokya ni edgar'
TEMPLATES_AUTO_RELOAD = True

# gunicorn -w 3 --log-level info --log-file=- run:app -b 127.0.0.1:8001