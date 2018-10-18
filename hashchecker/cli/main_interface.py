from hashchecker.core.coreactions.Calculate import Calculate
from hashchecker.core.coreactions.Duplicate import Duplicate
from hashchecker.core.coreactions.Verify import Verify
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
