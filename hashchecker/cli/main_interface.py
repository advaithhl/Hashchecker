from hashchecker.core.coreactions.Calculate import Calculate
from hashchecker.core.coreactions.Duplicate import Duplicate
from hashchecker.core.coreactions.Verify import Verify
from hashchecker.parsing.ArgParse import parse_args
from hashchecker.parsing.FileObjectParser import FileObjectParser
from hashchecker.cli.color_string import *

def perform(args: FileObjectParser): 
    if args.action_name == 'verify':
        verify_cli(args)
    elif args.action_name == 'calculate':
        calculate_cli(args)
    elif args.action_name == 'duplicate':
        duplicate_cli(args)


def verify_cli(args):
    hash_dict = {}
    v = Verify()
    print('Please enter the checksums of the files below')
    for file_object in args.get_file_objects():
        hash_dict[file_object] = input(file_object.get_name()+': ')
    print('Calculating')
    results = v.verify_all(hash_dict)
    print('All files have been verified!')

    pretty_result = lambda file_name, result: green(
        file_name + ' is OKAY!') if result else red(file_name + ' is NOT OKAY!')

    for (file_name, result) in results.items():
        print(pretty_result(file_name, result))


def calculate_cli(args):
    hashtypes = []
    for hashtype in parse_args().hashtypes:
        if hashtype == 'md5':
            hashtypes.append(Calculate.md5)
        elif hashtype == 'sha1':
            hashtypes.append(Calculate.sha1)
        elif hashtype == 'sha256':
            hashtypes.append(Calculate.sha256)
        elif hashtype == 'sha512':
            hashtypes.append(Calculate.sha512)

    c = Calculate()
    for result in c.calculate(hashtypes):
        print('file: {}\n+ md5: {}\n+ sha1: {}\n+ sha256: {}\n+ sha512: {}'.format(
            blue(result.file_object.get_name()),
            result.md5,
            result.sha1,
            result.sha256,
            result.sha512
        ))

def duplicate_cli(args):
    d = Duplicate()
    duplicate_count = len(d.get_duplicates())
    if duplicate_count:
        print('\n' + red('I found {} files which have duplicate copies'.format(duplicate_count)))    
    else:
        print('\n' + green('No duplicate files found.'))
        exit()
    
    for (count, duplicate_list) in enumerate(d.get_duplicates()):
        print('\n' + blue('Duplicates #{}'.format(count+1)))
        for file_name in duplicate_list:
            print('+', file_name)
