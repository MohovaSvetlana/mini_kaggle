import click

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db/kaggle.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_db():
    Base.metadata.create_all(bind=engine)


def close_db(e=None):
    db_session.remove()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
