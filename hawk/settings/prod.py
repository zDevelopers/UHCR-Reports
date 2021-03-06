import pymysql  # noqa - only installed on the production server
import sentry_sdk  # noqa - only installed on the production server
import toml

from sentry_sdk.integrations.django import DjangoIntegration  # noqa - only installed on the production server

from .base import *  # noqa

config_path = os.environ.get("HAWK_CONFIG", str(BASE_DIR / "config.toml"))

try:
    config = toml.load(config_path)
    print(f"Using the config file at {config_path!r}")
except OSError:
    config = {}

DEBUG = False

ALLOWED_HOSTS = config.get("allowed_hosts", ['hawk.carrade.eu'])
SECRET_KEY = config["secret_key"]

CONTENTS_DIR = Path(config.get("contents_dir", BASE_DIR / ".." / "hawk-data"))
LOGS_DIR = Path(config.get("logs_dir", CONTENTS_DIR / "logs"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config["databases"]["default"].get("name", "hawk"),
        "USER": config["databases"]["default"].get("user", "hawk"),
        "PASSWORD": config["databases"]["default"]["password"],
        "HOST": config["databases"]["default"].get("host", ""),
        "PORT": config["databases"]["default"].get("port", ""),
        "CONN_MAX_AGE": 600,
        "init_command": "SET sql_modes = 'STRICT_TRANS_TABLES'",
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    },
}

# Enable PyMySQL compatibility layer, as Django expect MySQLdb (from
# mysqlclient), but it's a pain to install on CentOS.
pymysql.version_info = (2, 0, 3, "final", 0)
pymysql.install_as_MySQLdb()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / "django.log",
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'WARNING',
    }
}

if "sentry_dsn" in config and config["sentry_dsn"]:
    sentry_sdk.init(
        dsn=config["sentry_dsn"],
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # As we don't really have users (at least for non-administrative
        # users), it's pointless to send PII data with requests.
        send_default_pii=False
    )

STATIC_ROOT = CONTENTS_DIR / "static"
MEDIA_ROOT = CONTENTS_DIR / "user-generated-content"
MAINTENANCE_MODE_STATE_FILE_PATH = CONTENTS_DIR / "maintenance"
