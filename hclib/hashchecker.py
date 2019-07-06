import textwrap
from os import path as os_path
from shutil import get_terminal_size

import click
from colorama import Fore as fgc
from tabulate import tabulate

import hclib.help_strings as hs
from hclib.core.core_actions import calculate, find_duplicates, verify
from hclib.core.core_objects import CHECKSUMS, DirectoryObject, FileObject


@click.group(
    help=hs.cli_help,
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
def cli_calculate(arg_list, checksums, hidden):
    """
    CLI Interface of the `calculate` command.

    First, files and directories are classified into separate lists. Missing
    files and directories are reported.
    """
    files = []
    dirs = []
    cols, rows = get_terminal_size()
    for arg in arg_list:
        if os_path.isfile(arg):
            files.append(FileObject(arg))
        elif os_path.isdir(arg):
            dirs.append(DirectoryObject(arg))
        else:
            print(f"- I did not find a file named '{arg}'")
    if files or dirs:
        for checksum in checksums:
            print('-' * ((cols-len(checksum))//2-1), end='')
            print(' '+checksum.upper()+' ', end='')
            print('-' * ((cols-len(checksum))//2-1))
            headers = ['Filename', checksum.upper()]
            if files:
                print(
                    f'\n+ Calculating {checksum} of given file(s)...',
                    end='', flush=True)
                result = calculate(files, checksum)
                print('\r+ FILES' + ' ' * 39)
                table = {
                    textwrap.fill(k.name, cols//2-4): textwrap.fill(v, cols//2-3)
                    for (k, v) in result.items()
                }
                print(tabulate(table.items(), headers, tablefmt="fancy_grid"))
            for d in dirs:
                print(
                    f'\n+ Calculating {checksum} of files in {d.path}...', end='', flush=True)
                dir_result = calculate(d.file_objects(
                    show_hidden=hidden), checksum)
                print(f'\r+ DIRECTORY: {d.path}' + ' ' * 22)
                table = {
                    textwrap.fill(k.name, cols//2-4): textwrap.fill(v, cols//2-3)
                    for (k, v) in dir_result.items()
                }
                print(tabulate(table.items(), headers, tablefmt="fancy_grid"))
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
def cli_verify(arg_list):
    print('+ I will automatically identify these checksums:', CHECKSUMS)
    print('+ Please enter any of the above checksum for each file\n')
    cols, rows = get_terminal_size()
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

    headers = ['Filename', 'Status']
    table = {
        textwrap.fill(k.name, cols//2-4): y_or_n(v)
        for (k, v) in result.items()
    }
    print(tabulate(table.items(), headers, tablefmt="fancy_grid"))


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
    '-d', '--directory',
    is_flag=True,
    help=hs.find_duplicates_directory_help,
)
def cli_find_duplicates(arg_list, directory):
    duplicates = None
    if directory:
        if len(arg_list) > 1:
            raise click.ClickException(
                '- Please provide either a single directory or list of files.'
                '\n- For more help, type hashchecker find_duplicates --help')
        else:
            dir_object = DirectoryObject(arg_list[0])
            if not dir_object.exists:
                print(
                    f"- I did not find a directory named '{dir_object.path}'")
                exit(1)
            print('+ Checking for duplicates files in the directory:',
                  arg_list[0], flush=True)
            duplicates = find_duplicates(DirectoryObject(arg_list[0]))
    else:
        try:
            print('+ Checking for duplicates among the given files...')
            list_of_file_objects = []
            for arg in arg_list:
                f = FileObject(arg)
                if not f.exists:
                    print(f"- I did not find a file named '{arg}'")
                    continue
                list_of_file_objects.append(f)
            if not list_of_file_objects:
                exit(1)
            duplicates = find_duplicates(list_of_file_objects)
        except IsADirectoryError as iade:
            print(f'? Sorry, but {iade}\n'
                  '? Please give -d option if you are specifying a directory')
            exit(1)
    if not duplicates:
        print(fgc.GREEN + '+ No duplicate files found!' + fgc.RESET)
    else:
        print(
            f'\n+ Found {fgc.RED + str(len(duplicates)) + fgc.RESET} cases of duplicate files.')
    cols, rows = get_terminal_size()
    headers = ['Index', 'Duplicates']
    for (file_object, duplicates) in duplicates.items():
        table = {
            textwrap.fill(str(idx + 1), cols//2-4): textwrap.fill(f.path, cols//2-3)
            for idx, f in enumerate(duplicates)
        }
        print('\n+ File: ', file_object.path)
        print(tabulate(table.items(), headers, tablefmt="fancy_grid"))
