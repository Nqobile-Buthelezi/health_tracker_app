import click
from app import db, User


# Command to view data from the database
@click.command()
def view_db():
    """Fetches and displays data from the database."""
    try:
        with db.app.app_context():
            all_users = User.query.all()
            if all_users:
                for user in all_users:
                    print(f"Username: {user.username}, Email: {user.email}")
            else:
                print("No users found in the database table.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Command to purge all data from the database
@click.command()
@click.option('--confirm', is_flag=True, help="Required confirmation to delete all data.")
def purge_db(confirm):
    """Deletes ALL data from the database. Use with extreme caution."""
    if not confirm:
        click.echo("Warning: This will permanently delete all data. Use '--confirm' to proceed.")
        return

    try:
        with db.app.app_context():
            db.reflect()  # Required to reflect tables from app metadata
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
            click.echo("Database cleared successfully.")
    except Exception as e:
        click.echo(f"An error occurred during database purge: {e}")
        db.session.rollback()


# Register commands with the Flask CLI
@click.group()
def database_cli():
    pass


database_cli.add_command(view_db)
database_cli.add_command(purge_db)
