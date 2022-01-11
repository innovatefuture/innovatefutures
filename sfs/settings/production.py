# pyre-strict

from .base import *
from django.conf import settings
from typing import List, Any
from django.core.handlers.wsgi import WSGIRequest

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = False


# SECRET_KEY: str = 'Q%Ohhtu$DbbtCvJMaspG31Ijsx0piYLAI4gUNpyxzpRVuxaUlbn(XKW'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS: List[str] = ['dev.sharedfutures.space', 'sharedfutures.space', '127.0.0.1', '0.0.0.0']

# just to fix some warnings, becomes relevant in next django version apparently
DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

# needed for oauth
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'

# number of supporters required for an idea to become a project
PROJECT_REQUIRED_SUPPORTERS = 5

try:
    from .local import *
except ImportError:
    pass
