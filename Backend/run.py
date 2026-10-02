"""
Main entry point for starting the Flask API. Initializes the database and starts the server.
"""

from app import create_app
from app.db.schema import init_db

app = create_app()

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run()