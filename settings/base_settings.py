"""
Django settings for interview project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

env.read_env(f'{BASE_DIR}/envs/.env.{env.str("PROJECT_ENV", "dev")}')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'rest_framework',
    # django-cid应用(日志请求，记录唯一id)
    'cid.apps.CidAppConfig',
    'area',
    'utils',
    # 查询过滤
    'django_filters'
]

MIDDLEWARE = [
    # 日志唯一ID生成(django-cid)，中间件负责从 HTTP 请求标头获取相关属性
    'cid.middleware.CidMiddleware',
    # 日志处理中间件(记录请求日志信息)
    'middleware.log_middleware.LogMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interview.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'interview.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'interview',
        'URL': env.str('DATABASES_URL'),
        'USER': env.str('DATABASE_USER'),
        'PORT': env.int('DATABASE_PORT'),
        'PASSWORD': env.str('DATABASE_PASSWORD'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 用户模型类
AUTH_USER_MODEL = 'user.User'

# ------------celery配置项------------------
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_BROKER_URL = env.str('BROKER_URL')
# BACKEND配置，这里使用redis
CELERY_RESULT_BACKEND = env.str('RESULT_BACKEND')
# 结果序列化方案
CELERY_RESULT_SERIALIZER = 'json'

# CELERYBEAT_SCHEDULER = 'celery.schedulers.DatabaseScheduler'  # 使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中

CELERY_TASK_RESULT_EXPIRES = 1200  # celery任务执行结果的超时时间，我的任务都不需要返回结果,只需要正确执行就行

CELERYD_CONCURRENCY = 10  # celery worker的并发数 也是命令行-c指定的数目,事实上实践发现并不是worker也多越好,保证任务不堆积,加上一定新增任务的预留就可以

CELERYD_PREFETCH_MULTIPLIER = 4  # celery worker 每次去rabbitmq取任务的数量，我这里预取了4个慢慢执行,因为任务有长有短没有预取太多

CELERYD_MAX_TASKS_PER_CHILD = 200  # 每个worker执行了多少任务就会死掉

CELERY_DEFAULT_QUEUE = "default_wj"  # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_TASK_SERIALIZER = 'json'

# -------------------百度OCR相关配置-------------------------
APP_ID = '28335545'
API_KEY = 'cZGotxafOdK8ThvYIuuOaGHs'
OCR_SECRET_KEY = 'PvckkIsoxSeVUz1qSGmplKBELqthOBpv'


# ----------------Django Rest Frame work相关的配置--------------
REST_FRAMEWORK = {
    # 默认的分页器
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 每页的个数
    'PAGE_SIZE': 10,
    # 默认的过滤器后端
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}

# ---------------Django-Cid配置----------------------------------
# https://django-correlation-id.readthedocs.io/en/latest/installation.html
CID_GENERATE = True  # 默认情况下使用uuid4生成
CID_RESPONSE_HEADER = 'Request-ID'
CID_HEADER = CID_RESPONSE_HEADER


# --------------日志相关配置-------------------------------
# 日志文件的存放路径(不存在就创建)
LOG_DIR = BASE_DIR / 'logs'
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[cid: %(cid)s] %(levelname)s %(asctime)s %(message)s'
        },
        'simple': {
            'format': '[cid: %(cid)s] %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'api_request_handler': {
            'level': 'INFO',
            'class': 'utils.log_file_handler.CommonTimedRotatingFileHandler',
            'formatter': 'verbose',
            'filters': ['correlation'],
            'filename': 'logs/api_request.log',
            # 每分钟切割一次日志
            'when': 'midnight',
            # 时间间隔
            'interval': 1,
            # 保留5份日志
            'backupCount': 30,
            'encoding': 'utf-8'
        },
    },
    'filters': {
        'correlation': {
            '()': 'cid.log.CidContextFilter'
        },
    },
    'loggers': {
        'api_request': {
            'handlers': ['api_request_handler'],
            'filters': ['correlation'],
            'propagate': True,
            'level': 'INFO'
        },
    },
}

# ----------------sentry配置-------------------------
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
dsn="http://895fa50f68214d3ab2700de2ef915c69@127.0.0.1:9000/3",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
