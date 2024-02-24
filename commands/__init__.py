import click
from flask.cli import with_appcontext
from app import db


@click.command()
@with_appcontext
def init_db():
    """Initialise the database."""
    db.create_all()
    click.echo("Initialised the database.")
