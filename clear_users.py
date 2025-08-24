from app.database import SessionLocal
from app.models import User, Client

def clear_users_and_clients():
    db = SessionLocal()
    try:
        # сначала чистим клиентов
        deleted_clients = db.query(Client).delete()
        print(f"Удалено клиентов: {deleted_clients}")

        # потом чистим пользователей
        deleted_users = db.query(User).delete()
        print(f"Удалено пользователей: {deleted_users}")

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    clear_users_and_clients()
