#!/usr/bin/env python3
import subprocess

import click

from linkscutter.controllers import wsgi  # noqa


@click.group()
def cli():
    pass


@cli.command()
def runserver():
    wsgi.init()
    wsgi.app.run(debug=True, reloader=True)


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
@click.option('--count', '-c', default=100, help='Number of users')
@click.option('--deep', '-d', default=10, help='Max number of items')
def fill(count, deep):
    # from faker import Factory
    # faker = Factory.create()
    pass


if __name__ == '__main__':
    cli()
