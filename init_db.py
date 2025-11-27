from app import app
from models_fixed import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Database created (if not existing).')
