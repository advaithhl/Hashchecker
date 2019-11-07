import textwrap
from os import path as os_path
from shutil import get_terminal_size

import click
import hclib.help_strings as hs
import pkg_resources
from colorama import Fore as fgc
from hclib.core.core_actions import calculate, find_duplicates, verify
from hclib.core.core_objects import CHECKSUMS, DirectoryObject, FileObject
from tabulate import tabulate

cols, rows = get_terminal_size()


def get_files_dirs(arg_list):
    files = []
    dirs = []
    for arg in arg_list:
        if os_path.isfile(arg):
            files.append(FileObject(arg))
        elif os_path.isdir(arg):
            dirs.append(DirectoryObject(arg))
        else:
            print(f"- I did not find a file named '{arg}'")
    return files, dirs


def get_version():
    version = pkg_resources.require("hashchecker")[0].version
    return version


def pretty_table_left(key):
    return textwrap.fill(key, cols//2-4)


def pretty_table_right(value):
    return textwrap.fill(value, cols//2-3)


def pretty_print(table, headers):
    TABLE_FMT = 'fancy_grid'
    print(tabulate(table.items(), headers, tablefmt=TABLE_FMT))


@click.group(
    help=hs.cli_help,
)
@click.version_option(
    version=get_version(),
    prog_name="Hashchecker"
)
def cli():
    """
    Entry point for CLI commands
    """
    pass


@cli.command(
    'calculate',
    help=hs.calculate_help,
)
@click.argument(
    'arg_list',
    required=True,
    nargs=-1,
)
@click.option(
    '-c', '--checksum',
    'checksums',
    type=click.Choice(CHECKSUMS),
    default=['sha256'],
    multiple=True,
    help=hs.calculate_checksum_help,
)
@click.option(
    '-x', '--hidden',
    is_flag=True,
    help=hs.calculate_hidden_help,
)
@click.option(
    '-t', '--plaintext',
    is_flag=True,
    help=hs.plaintext_help,
)
def cli_calculate(arg_list, checksums, hidden, plaintext):
    """
    CLI Interface of the `calculate` command.

    First, files and directories are classified into separate lists. Missing
    files and directories are reported.
    """
    files, dirs = get_files_dirs(arg_list)
    global cols, rows
    if files or dirs:
        for checksum in checksums:
            print('-' * ((cols-len(checksum))//2-1), end='')
            print(' '+checksum.upper()+' ', end='')
            print('-' * ((cols-len(checksum))//2-1))
            if files:
                print(
                    f'\n+ Calculating {checksum} of given file(s)...',
                    end='', flush=True)
                result = calculate(files, checksum)
                print('\r+ FILES' + ' ' * 39)
                if plaintext:
                    for (file_object, file_checksum) in result.items():
                        print(f'{file_object.fspath}: {file_checksum}')
                else:
                    headers = ['Filename', checksum.upper()]
                    table = {
                        pretty_table_left(k.name): pretty_table_right(v)
                        for (k, v) in result.items()
                    }
                    pretty_print(table, headers)
            for d in dirs:
                print(
                    f'\n+ Calculating {checksum} of files in {d.path}...', end='', flush=True)
                dir_result = calculate(d.file_objects(
                    show_hidden=hidden), checksum)
                print(f'\r+ DIRECTORY: {d.path}' + ' ' * 22)
                # dir_result might be empty if there aren't any files in d
                if not dir_result:
                    print(
                        "\n\t- I didn't find any files here. "
                        "Note that I did not traverse possible subdirectories.")
                    continue
                if plaintext:
                    for (file_object, file_checksum) in dir_result.items():
                        print(f'{file_object.name}: {file_checksum}')
                else:
                    table = {
                        pretty_table_left(k.name): pretty_table_right(v)
                        for (k, v) in dir_result.items()
                    }
                    pretty_print(table, headers)
            print('-' * cols)


@cli.command(
    'verify',
    help=hs.verify_help,
)
@click.argument(
    'arg_list',
    required=True,
    nargs=-1,
)
@click.option(
    '-t', '--plaintext',
    is_flag=True,
    help=hs.plaintext_help,
)
def cli_verify(arg_list, plaintext):
    print('+ I will automatically identify these checksums:', CHECKSUMS)
    print('+ Please enter any of the above checksum for each file\n')
    global cols, rows
    l = []
    correct_checksums = []
    for arg in arg_list:
        try:
            f = FileObject(arg)
            if not f.exists:
                print(f"- I did not find a file named '{arg}'")
                continue
            l.append(f)
            c = input(f'{arg}: ')
            while len(c) not in (32, 40, 64, 128):
                print(f"? Sorry, this does not look like a valid checksum "
                      "produced by any of the supported algorithms:", CHECKSUMS)
                print("? Please verify the whether you have entered the actual "
                      f"checksum of \'{f.name}\'.\n")
                c = input(f'{arg}: ')
            correct_checksums.append(c)
        except IsADirectoryError as iade:
            print(iade)
    if not l:
        exit(1)
    print('\n+ Verifying... ', end='', flush=True)
    result = verify(l, correct_checksums)
    print('Done!')

    def y_or_n(x):
        if x:
            return fgc.GREEN + 'Valid' + fgc.RESET
        return fgc.RED + 'Corrupt' + fgc.RESET

    if plaintext:
        for (file_object, status) in result.items():
            print(file_object.fspath + ': ' + y_or_n(status))
    else:
        headers = ['Filename', 'Status']
        table = {
            pretty_table_left(k.name): pretty_table_right(y_or_n(v))
            for (k, v) in result.items()
        }
        pretty_print(table, headers)


@cli.command(
    'find_duplicates',
    help=hs.find_duplicates_help,
)
@click.argument(
    'arg_list',
    required=True,
    nargs=-1,
)
@click.option(
    '-t', '--plaintext',
    is_flag=True,
    help=hs.plaintext_help,
)
def cli_find_duplicates(arg_list, plaintext):
    duplicates = None
    files, dirs = get_files_dirs(arg_list)
    global cols, rows
    duplicates = find_duplicates(files, dirs)
    if not duplicates:
        print(fgc.GREEN + '+ No duplicate files found!' + fgc.RESET)
    else:
        print(
            f'\n+ Found {fgc.RED + str(len(duplicates)) + fgc.RESET} case(s) of duplicate files.')
        for (file_object, duplicates) in duplicates.items():
            if plaintext:
                print('\n+ File:', file_object.path)
                for (idx, f) in enumerate(duplicates, start=1):
                    print(f'{idx}. {f.path}')
            else:
                table = {
                    pretty_table_left(str(idx)): pretty_table_right(f.path)
                    for idx, f in enumerate(duplicates, start=1)
                }
                headers = ['Index', 'Duplicates']
                pretty_print(table, headers)


if __name__ == '__main__':
    cli()
