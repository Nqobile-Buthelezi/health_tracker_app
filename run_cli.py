from app import app
from app.database import database_cli

if __name__ == "__main__":
    database_cli()  # Registers my database commands with Flask CLI
    app.run(debug=True)
