"""
Django settings for interview project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os

from pathlib import Path
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

env.read_env(f'{BASE_DIR}/envs/.env.{env.str("PROJECT_ENV", "dev")}')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "rest_framework",
    # django-cid应用(日志请求，记录唯一id)
    "cid.apps.CidAppConfig",
    "area",
    "utils",
    "analysis",  # 数据分析模块
    "django_filters",
    "chat",  # django-channels的网络聊天室
    "django_elasticsearch_dsl",  # django-elasticsearch-dsl
]

MIDDLEWARE = [
    # 日志处理中间件(记录请求日志信息)
    "middleware.log_middleware.LogMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 日志唯一ID生成(django-cid)，中间件负责从 HTTP 请求标头获取相关属性
    "cid.middleware.CidMiddleware",
]

ROOT_URLCONF = "interview.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "interview.wsgi.application"
ASGI_APPLICATION = "interview.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "interview",
        "URL": env.str("DATABASES_URL"),
        "USER": env.str("DATABASE_USER"),
        "PORT": env.int("DATABASE_PORT"),
        "PASSWORD": env.str("DATABASE_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
# 静态文件的存放目录
STATIC_ROOT = "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 用户模型类
AUTH_USER_MODEL = "user.User"

# ------------celery配置项------------------
# 设置celery的时区
CELERY_TIMEZONE = "Asia/Shanghai"
# 设置celery broker(存储任务的)的地址
CELERY_BROKER_URL = env.str("BROKER_URL")
# BACKEND配置(存储结果),使用redis
CELERY_RESULT_BACKEND = env.str("RESULT_BACKEND")
# 结果序列化方案
CELERY_RESULT_SERIALIZER = "json"
# 使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中
# CELERYBEAT_SCHEDULER = 'celery.schedulers.DatabaseScheduler'
# 存储任务结果的过期时间，超过这个时间自动过期，设置为None，表示永久有效
CELERY_TASK_RESULT_EXPIRES = 1200
# 每个worker可以同时处理的任务数量，默认是2，建议设置为当前电脑的核心数
CELERYD_CONCURRENCY = os.cpu_count()
# 用于控制worker进程每次从broker中预取任务的数量，默认是4
CELERYD_PREFETCH_MULTIPLIER = 4
# 它用于控制每个worker进程最多可以处理的任务数量。一旦worker进程处理任务的数量达到这个值，就会重启
CELERYD_MAX_TASKS_PER_CHILD = 200
# 如果消息没有指定路由或者没有指定队列，都将放到默认队列中
CELERY_DEFAULT_QUEUE = "default_wj"
# 允许接受的内容类型，如果不符合该类型，则任务会被丢弃，支持的类型有json，YAML， pickle等
CELERY_ACCEPT_CONTENT = ["application/json"]
# 任务信息的序列化方式
CELERY_TASK_SERIALIZER = "json"

# -------------------百度OCR相关配置-------------------------
APP_ID = "28335545"
API_KEY = "cZGotxafOdK8ThvYIuuOaGHs"
OCR_SECRET_KEY = "PvckkIsoxSeVUz1qSGmplKBELqthOBpv"


# ----------------Django Rest Frame work相关的配置--------------
REST_FRAMEWORK = {
    # 默认的分页器
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # 每页的个数
    "PAGE_SIZE": 10,
    # 默认的过滤器后端
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    # 全局错误处理钩子函数
    "EXCEPTION_HANDLER": "utils.exception.custom_exception_handler",
    # 自定义响应格式
    "DEFAULT_RENDERER_CLASSES": ("utils.response.custom_renderer",),
}

# ---------------Django-Cid配置----------------------------------
# https://django-correlation-id.readthedocs.io/en/latest/installation.html
CID_GENERATE = True  # 默认情况下使用uuid4生成
CID_RESPONSE_HEADER = "Request-ID"
CID_HEADER = CID_RESPONSE_HEADER


# --------------日志相关配置-------------------------------
# 日志文件的存放路径(不存在就创建)
LOG_DIR = BASE_DIR / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir()

LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "[cid: %(cid)s] %(levelname)s %(asctime)s %(module)s %(message)s"
        },
        "simple": {"format": "[cid: %(cid)s] %(levelname)s %(message)s"},
    },
    "handlers": {
        "api_handler": {
            "level": "INFO",
            "class": "utils.log_file_handler.KafkaLoggingHandler",
            "formatter": "verbose",
            "filters": ["correlation"],
            "filename": f"{BASE_DIR}/logs/api_request.log",
            # 每分钟切割一次日志
            "when": "midnight",
            # 时间间隔
            "interval": 1,
            # 保留5份日志
            "backupCount": 30,
            "encoding": "utf-8",
        },
    },
    "filters": {
        "correlation": {"()": "cid.log.CidContextFilter"},
    },
    "loggers": {
        "api": {
            "handlers": ["api_handler"],
            "filters": ["correlation"],
            "propagate": True,
            "level": "INFO",
        },
    },
}

# ----------------sentry配置-------------------------
sentry_sdk.init(
    dsn="http://895fa50f68214d3ab2700de2ef915c69@127.0.0.1:9000/3",
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


# -------------django-channels通道层配置-----------------
# 使用redis作为通道的存储介质
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://:1277431229@127.0.0.1:6379/4")],
        },
    },
}

# Elasticsearch配置
ELASTICSEARCH_DSL = {
    "default": {"hosts": "localhost:9200"},
}
