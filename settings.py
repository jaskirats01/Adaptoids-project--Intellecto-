INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'speech_app',
]

CORS_ALLOW_ALL_ORIGINS = True  # Allow React frontend to access Django API

AWS_ACCESS_KEY = "your_aws_access_key"
AWS_SECRET_KEY = "your_aws_secret_key"
AWS_REGION = "us-east-1"
AWS_S3_BUCKET = "your-s3-bucket-name"