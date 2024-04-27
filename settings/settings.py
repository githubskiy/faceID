from envparse import Env

env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:1243@127.0.0.1:5432/mydata"
)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)


# Milvus server IP address and port.
_HOST = '127.0.0.1'
_PORT = '19530'  # default value

# Vector parameters
_DIM = 512  # dimension of vector
_INDEX_FILE_SIZE = 32  # max file size of stored index