import click
from changesetdb.database import Database


@click.group()
@click.option('-d', '--dbname')
@click.option('-h', '--host')
@click.option('-p', '--port')
@click.option('-U', '--username')
@click.pass_context
def cli(ctx, dbname, host, port, username):
    ctx.obj = Database(dbname, host, port, username)


@cli.command()
@click.pass_context
def create(ctx):
    ctx.obj.createtables()


@cli.command()
@click.pass_context
def drop(ctx):
    ctx.obj.droptables()
