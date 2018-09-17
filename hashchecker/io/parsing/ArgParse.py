import click

__parsed_files = None
__hash_types = None


@click.group()
def main_action():
    pass


@main_action.command()
@click.argument('files', nargs=-1)
def verify(files):
    global __parsed_file
    __parsed_file = files


@main_action.command()
@click.argument('files', nargs=-1)
def duplicate(files):
    global __parsed_file
    __parsed_file = files


@main_action.command()
@click.argument('files', nargs=-1)
@click.option('-h', '--hashtype', multiple=True, type=click.Choice(['md5', 'sha1', 'sha256', 'sha512']))
def calculate(files, hashtype):
    global __parsed_file
    __parsed_file = files
    global __hash_types
    __hash_types = hashtype


def parsed_files():
    return __parsed_files


def hash_types():
    return __hash_types
