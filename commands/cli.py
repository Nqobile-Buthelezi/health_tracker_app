import os
import sys
import click
import pandas as pd


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get the absolute path to the Flask application directory from the environment variable
flask_app_path = os.getenv("FLASK_APP_PATH")

# Add the Flask application directory to the system path
sys.path.append(flask_app_path)

# Now you can import your Flask app
from app import app as flask_app
from run import run_app


@click.command()
def view_db():
    """Fetches and displays data from the database."""
    try:
        all_users = flask_app.User.query.all()
        if all_users:
            for user in all_users:
                print(f"Username: {user.username}, Email: {user.email}")
        else:
            print("No users found in the database table.")
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        raise click.Abort()


# Command to purge all data from the database
@click.command()
@click.option('--confirm', is_flag=True, help="Required confirmation to delete all data.")
def purge_db(confirm):
    """Deletes ALL data from the database. Use with extreme caution."""
    if not confirm:
        click.echo("Warning: This will permanently delete all data. Use '--confirm' to proceed.")
        return

    try:
        with flask_app.app.app_context():
            flask_app.db.reflect()  # Required to reflect tables from app metadata
            for table in reversed(flask_app.db.metadata.sorted_tables):
                flask_app.db.session.execute(table.delete())
            flask_app.db.session.commit()
            click.echo("Database cleared successfully.")
    except Exception as e:
        click.echo(f"An error occurred during database purge: {e}")
        flask_app.db.session.rollback()


# Command to export data from the database to a CSV file
@click.command()
@click.argument('output_file', type=click.Path())
def export_csv(output_file):
    """Exports data from the database to a CSV file."""
    try:
        with flask_app.app.app_context():
            all_users = flask_app.User.query.all()
            df = pd.DataFrame([(user.id, user.username, user.email) for user in all_users],
                              columns=['ID', 'Username', 'Email'])
            df.to_csv(output_file, index=False)
            click.echo(f"Data exported to {output_file} successfully.")
    except Exception as e:
        click.echo(f"An error occurred during export: {e}")


# Command to import data from a CSV file into the database
@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def import_csv(input_file):
    """Imports data from a CSV file into the database."""
    try:
        with flask_app.app.app_context():
            df = pd.read_csv(input_file)
            for _, row in df.iterrows():
                user = flask_app.User(username=row['Username'], email=row['Email'])
                flask_app.db.session.add(user)
            flask_app.db.session.commit()
            click.echo("Data imported successfully.")
    except Exception as e:
        click.echo(f"An error occurred during import: {e}")


@click.command()
def run():
    """Runs the default configuration of the flask Application."""
    run_app(flask_app.app)


# Register commands with the Flask CLI
@click.group()
def database_cli():
    pass


database_cli.add_command(view_db)
database_cli.add_command(purge_db)
database_cli.add_command(import_csv)
database_cli.add_command(export_csv)
database_cli.add_command(run)

if __name__ == "__main__":
    database_cli()
