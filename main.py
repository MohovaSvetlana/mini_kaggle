from data.db import init_db
from data.app_init import create_app

if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run()
else:
    gunicorn_app = create_app()
