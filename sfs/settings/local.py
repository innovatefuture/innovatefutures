# pyre-strict
# all auth details
#import apps.userauth.views

from typing import List, Optional

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = 'Q%Ohhtu$DbbtCvJMaspG31Ijsx0piYLAI4gUNpyxzpRVuxaUlbn(XKW'

SITE_ID = 1
SITE_DOMAIN = 'sharedfutures.space'

AUTHENTICATION_BACKENDS: List[str] = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


LOGIN_REDIRECT_URL: str = '/dashboard/'
LOGOUT_REDIRECT_URL: str = '/'
LOGIN_URL: str = '/account/login/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL: Optional[str] = LOGIN_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL: Optional[str] = None

ACCOUNT_AUTHENTICATION_METHOD: str = 'email'
ACCOUNT_EMAIL_REQUIRED: bool = True
ACCOUNT_EMAIL_VERIFICATION: str = 'mandatory'
ACCOUNT_USERNAME_REQUIRED: bool = False
ACCOUNT_UNIQUE_EMAIL = True

EMAIL_HOST: str = 'mail.webarch.net'
EMAIL_PORT: int = 465
EMAIL_HOST_USER: str = 'sfs_mailer@animorph.coop'
EMAIL_HOST_PASSWORD: str = '7{zjA+b!xWLe5i>C[)U6jOx<gQe(x9g'
EMAIL_USE_TLS: bool = False
EMAIL_USE_SSL: bool = True
DEFAULT_FROM_EMAIL: str = EMAIL_HOST_USER

# custom user model
AUTH_USER_MODEL: str = 'userauth.CustomUser'

#overriding default account
ACCOUNT_ADAPTER: str = 'userauth.views.CustomAllauthAdapter'
SOCIALACCOUNT_ADAPTER = 'userauth.adapters.CustomSocialAccountAdapter'

# pickle required to serialize and send EmailMultiAlternatives
# https://docs.celeryproject.org/en/latest/userguide/calling.html#calling-serializers
CELERY_ACCEPT_CONTENT: List[str] = ['pickle']
CELERY_TASK_SERIALIZER: str = 'pickle'
CELERY_RESULT_SERIALIZER: str = 'pickle'
