
import os

# mysql config
MYSQL_DB_PWD = os.getenv("MYSQL_DB_PWD", "123456")
MYSQL_DB_USER = os.getenv("MYSQL_DB_USER", "root")
MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST", "localhost")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT", 3306)
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME", "media_crawler")

mysql_db_config = {
    "user": MYSQL_DB_USER,
    "password": MYSQL_DB_PWD,
    "host": MYSQL_DB_HOST,
    "port": MYSQL_DB_PORT,
    "db_name": MYSQL_DB_NAME,
}


# redis config
REDIS_DB_HOST = os.getenv("REDIS_DB_HOST", "127.0.0.1")  # your redis host
REDIS_DB_PWD = os.getenv("REDIS_DB_PWD", "123456")  # your redis password
REDIS_DB_PORT = os.getenv("REDIS_DB_PORT", 6379)  # your redis port
REDIS_DB_NUM = os.getenv("REDIS_DB_NUM", 0)  # your redis db num

# cache type
CACHE_TYPE_REDIS = "redis"
CACHE_TYPE_MEMORY = "memory"

# sqlite config
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "sqlite_tables.db")

sqlite_db_config = {
    "db_path": SQLITE_DB_PATH
}

# postgres config
POSTGRES_DB_PWD = os.getenv("POSTGRES_DB_PWD", "123456")
POSTGRES_DB_USER = os.getenv("POSTGRES_DB_USER", "postgres")
POSTGRES_DB_HOST = os.getenv("POSTGRES_DB_HOST", "localhost")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT", 5432)
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "media_crawler")

postgres_db_config = {
    "user": POSTGRES_DB_USER,
    "password": POSTGRES_DB_PWD,
    "host": POSTGRES_DB_HOST,
    "port": POSTGRES_DB_PORT,
    "db_name": POSTGRES_DB_NAME,
}
