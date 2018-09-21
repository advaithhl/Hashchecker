from threading import Thread

import click


class ArgParse:

    def __init__(self,
                 action=None,
                 parsed_files=None,
                 hashtypes=None):
        self.main_action = action
        self.parsed_files = parsed_files
        self.hashtypes = hashtypes


args = ArgParse()


def parse_args():
    t = Thread(target=main_action)
    t.start()
    t.join()
    return args


@click.group()
def main_action():
    pass


@main_action.command()
@click.argument('files', nargs=-1)
def verify(files):
    return ArgParse(action=verify,
                    parsed_files=files)


@main_action.command()
@click.argument('files', nargs=-1)
def duplicate(files):
    return ArgParse(action=duplicate,
                    parsed_files=files)


@main_action.command()
@click.argument('files', nargs=-1)
@click.option('-h', '--hashtype', multiple=True, type=click.Choice(['md5', 'sha1', 'sha256', 'sha512']))
def calculate(files, hashtype):
    return ArgParse(action=calculate,
                    parsed_files=files,
                    hashtypes=hashtype)


@main_action.resultcallback()
def process_results(result):
    global args
    args = result
