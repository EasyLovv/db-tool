import click
from ..database import Base
from sqlalchemy import create_engine


@click.group()
@click.option('--host', '-h', default="localhost", help="PostgreSQL host.")
@click.option('--port', '-p', type=int, default=5432, help="PostgreSQL port.")
@click.option('--user', '-u', required=True, help="PostgreSQL user.")
@click.option('--password', required=True, help="PostgreSQL password.")
@click.option('--database', '-d', required=True, help="PostgreSQL base name.")
@click.option('--threads', '-t', type=int, default=1, help="The amount of threads which would "
                                                           "be used for pushing data to database")
@click.option('--bulk_size', '-b', type=int, default=100, help="The amount on entries for the one call.")
@click.pass_context
def call(ctx, host, port, user, password, database, threads, bulk_size):
    uri = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    ctx.obj["engine"] = create_engine(uri, pool_size=threads)
    ctx.obj["threads"] = threads
    ctx.obj["bulk_size"] = bulk_size


@call.command(name="create_db", help="Creates the tables described in the project `database` folder.")
@click.pass_context
def create_db(ctx, *args, **kwargs):
    Base.metadata.create_all(ctx.obj['engine'])
    click.echo("Done.")
