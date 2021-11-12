import argparse

from src import create_app, User, db

app = create_app()


def create_admin(username, password):
    with app.app_context():
        new_user = User(username=username, role="admin")
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()


parser = argparse.ArgumentParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
args = parser.parse_args()
create_admin(username=args.username, password=args.password)

