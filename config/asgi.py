import os

import dotenv
from django.core.asgi import get_asgi_application

dotenv.read_dotenv('.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = get_asgi_application()
