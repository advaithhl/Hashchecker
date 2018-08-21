import argparse


class ArgParse:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Description'
        )

        self.__main_action_group = self.parser.add_mutually_exclusive_group()

        self.__main_action_group.add_argument(
            '-v', '--verify',
            help='Verify files checksums',
            nargs='+'
        )

        self.__main_action_group.add_argument(
            '-c', '--calculate',
            help='Calculate file checksums',
            nargs='+'
        )

        self.__main_action_group.add_argument(
            '-r', '--redundancy',
            help='Check if any of the given files are duplicates of one another',
            nargs='+'
        )

        self.__output_group = self.parser.add_argument_group()
        self.__output_group.add_argument(
            '-o', '--output',
            help='Output results to file',
            nargs='?',
            const='CHECKSUMS',
            type=argparse.FileType('w')
        )

        self.args = self.parser.parse_args()
