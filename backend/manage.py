#!/usr/bin/env python3
import subprocess

import click

from linkscutter.application import LinkRepository  # noqa
from linkscutter.controllers import wsgi  # noqa
from linkscutter.utils import fill_fake_links  # noqa


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    wsgi.init().run(debug=True, reloader=True)


@cli.command()
def test():
    subprocess.call(['sh', './scripts/test.sh'])


@cli.command()
@click.option('--name', '-n', help='name of migration')
def makemigration(name):
    command = ['python', '-m', 'migrator', 'new']
    if name:
        command.append(name)
    subprocess.call(command)


@cli.command()
def migrate():
    subprocess.call(['python', '-m', 'migrator', 'apply'])


@cli.command()
@click.option('--count', '-c', default=100, help='Number of links')
def fill(count):
    fill_fake_links(LinkRepository(), count)


if __name__ == '__main__':
    cli()
