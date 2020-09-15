import sys
from flask.cli import FlaskGroup

from src import create_app, db
from src.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    print("recreate_db starts.")
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("recreate_db ends.")


@cli.command('seed_db')
def seed_db():
    print("seed_db starts.")
    db.session.add( User(username='hao', email="hao@gmail.com") )
    db.session.add( User(username='jeffrey', email="jeffrey@gmail.com") )
    db.session.commit()
    print("seed_db ends.")


if __name__ == '__main__':
    cli()
