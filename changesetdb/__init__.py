import click
from changesetdb.database import Database
from changesetdb.parser import Parser


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


@cli.command()
@click.argument('filename', type=click.File('rb'))
@click.pass_context
def load(ctx, filename):
    parser = Parser(False, ctx.obj)
    parser.load(filename)
