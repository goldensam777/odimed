import sys
from sqlmodel import Session, select
from app.core.db import engine
from app.models import User

def delete_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            session.delete(user)
        session.commit()
        print(f"Deleted {len(users)} users.")

if __name__ == "__main__":
    delete_all_users()
