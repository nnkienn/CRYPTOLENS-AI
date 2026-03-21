from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# IMPORT SQLMODEL VÀ MODELS CỦA ÔNG
from sqlmodel import SQLModel
from app.modules.crawler.models import Article  # Phải import cụ thể model để nó load vào metadata
from app.core.config import settings

# Alembic Config object
config = context.config

# Cấu hình logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# CHỖ ĂN TIỀN: Lấy URL từ Settings và đổi sang driver đồng bộ (psycopg2)
database_url = settings.DATABASE_URL.replace("asyncpg", "psycopg2")
config.set_main_option("sqlalchemy.url", database_url)

# CHỖ ĂN TIỀN 2: Chỉ định Metadata của SQLModel
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()