from sqlmodel import Session,select
from app.database import db_engine,setup_db
from app.models import Account
from app.enums import Role
from app.security import make_hash

def create_admin():
    setup_db()
    username=input("Admin username: ").strip()
    email=input("Admin email: ").strip()
    password=input("Admin password: ").strip()

    with Session(db_engine) as session:
        account=session.exec(select(Account).where(Account.username==username)).first()
        if account:
            print("Username is taken")
            return

        account=session.exec(select(Account).where(Account.email==email)).first()
        if account:
            print("Email is already registered")
            return

        admin=Account(username=username,email=email,hashed_password=make_hash(password),role=Role.admin)
        session.add(admin)
        session.commit()
        session.refresh(admin)
        print(f"Admin created with ID {admin.id}")

if __name__=="__main__":
    create_admin()