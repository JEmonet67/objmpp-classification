import click
import logging
import sys

from lib.main import main

@click.group()
def cli():
    """Command line utility"""
    # logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    pass

@click.command()
@click.argument('path_data')
@click.argument('path_images')
@click.option('--debug', is_flag=True, help="Will print debug messages.")
def organoid(path_data, path_images, debug=False):
    main(path_data, path_images, debug)

cli.add_command(organoid)

# if __name__ == "__main__":
#     sys.exit()

