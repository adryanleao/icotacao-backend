import datetime
import os

try:
    APP_ENV = str(os.environ["APP_ENV"])
except KeyError:
    APP_ENV = "development"

ROOT = os.path.dirname(os.path.abspath(__file__))


class Config:
    # app
    SITE_HTTPS = os.environ.get("SITE_HTTPS")
    SECRET_KEY = "c29jaWFsY29hY2g6Z2FsZGlubw=="
    JSON_SORT_KEYS = True

    # Key cryptography
    KEY_CRYPTOGRAPHY = "_oVz5CdXLmpGPkxoEIQcT_nPFDtIfVeFlLsGb58bcOI="

    # jwt
    JWT_SECRET_KEY = "c29jaWFsY29hY2h0d2o6Z2FsZGlubw=="
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRES = 3600
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=JWT_EXPIRES)

    # Flask RESTfull
    PROPAGATE_EXCEPTIONS = True

    # sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 0
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.environ.get("DB_USER", "root"),
        os.environ.get("DB_PASS", "root"),
        os.environ.get("DB_HOST", "sqlalchemy"),
        os.environ.get("DB_NAME", "sensi_db_init")
    )
    SQLALCHEMY_BINDS = {
        "slave": SQLALCHEMY_DATABASE_URI
    }

    # cache
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "simple")
    if CACHE_TYPE == "redis":
        CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST")
        CACHE_REDIS_PORT = os.environ.get("CACHE_REDIS_PORT")
        CACHE_KEY_PREFIX = SITE_HTTPS

    # aws
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_LOCATION = "us-east-1"
    AWS_BUCKET = "icotacao-files"
    AWS_BUCKET_LOCATION = AWS_LOCATION
    AWS_BUCKET_CLOUDFRONT = None

    # kraken
    KRAKEN_API_KEY = os.environ.get('KRAKEN_API_KEY')
    KRAKEN_API_SECRET = os.environ.get('KRAKEN_API_SECRET')
