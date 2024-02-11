# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Change this to match your database engine if you're not using Django
        'NAME': 'vitapulse_db',                 # Database name
        'USER': 'nqobile',                      # Database user
        'PASSWORD': 'nqobilesql',               # Database password
        'HOST': 'localhost',                    # Database host (usually 'localhost' for local development)
        'PORT': '3306',                         # Database port (default for MySQL is 3306)
    }
}
