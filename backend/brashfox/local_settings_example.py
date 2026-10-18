# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': '<tu wstaw nazwę bazy danych>',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': '<tu wstaw nazwę użytkownika bazy danych>',
        'PASSWORD': '<tu wstaW hasło bazy danych>',
        'HOST': '127.0.0.1'
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<tu wstaw swój sekret>'
