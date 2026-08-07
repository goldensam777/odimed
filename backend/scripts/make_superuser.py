import sys
from sqlmodel import Session, select
from app.core.db import engine
from app.models import User

def make_all_superusers():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            user.is_superuser = True
            session.add(user)
        session.commit()
        print(f"Updated {len(users)} users to superuser.")

if __name__ == "__main__":
    make_all_superusers()
