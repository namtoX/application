from kivy.utils import platform
import os

def get_db_path():
    if platform == 'android':
        from android.storage import app_storage_path
        app_path = app_storage_path()
        db_path = os.path.join(app_path, 'db.db')
    else:
        db_path = os.path.join(os.path.dirname(__file__), 'db.db')
    return db_path
