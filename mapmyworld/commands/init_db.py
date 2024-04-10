from mapmyworld.models import locations, categories, location_category_reviewed
from flask import current_app
from pprint import pprint
import click


@current_app.cli.command('init_db')
@click.pass_context
def run(ctx):
    try:
        click.echo(f"DB Iinicialidazada")
    except Exception as e:
        click.echo(str(e))
        ctx.exit(1)
    finally:
        ctx.exit(0)
