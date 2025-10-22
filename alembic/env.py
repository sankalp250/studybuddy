# In alembic/env.py

# Keep the existing top part of the file
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# This ensures that Alembic can find your 'studybuddy' package and its modules.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from studybuddy.core.config import settings
from studybuddy.database.connection import Base
# Make sure all of your models are imported here so Alembic can see them!
from studybuddy.database.models import User, StudyTopic, Todo

# 2. FIND AND EDIT THE 'config' SECTION
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# This line loads our database URL from our main application settings.
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. FIND THE 'target_metadata' VARIABLE AND CHANGE IT
# This tells Alembic that our models are defined using the 'Base' declarative class.
target_metadata = Base.metadata

# ==============================================================================
# --- END OF MODIFICATIONS (the rest of the file can be left as is) ---
# ==============================================================================

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.
    # ... (no changes needed below this line)
    """

    def process_revision_directives(context, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **config.attributes
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
