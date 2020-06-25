import click
from flask.cli import with_appcontext
from flaskblog import create_app, db


@click.command('init-db')
@with_appcontext
def init_db_command():
    """This function is used only once from command line for initial
    database setup when configuring the app in new environment
    """
    with create_app().app_context():
        db.create_all()
    click.echo('Initialized the database.')
