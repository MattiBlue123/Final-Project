import argparse


def config_args_parser():
    """
    Configure the parser for the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='get the path of the file or directory')
    parser.add_argument('path', type=str, help='path of the file or directory')
    parser.add_argument('unit_length', type=int, help='unit length')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = config_args_parser()
    print(args.unit_length, args.path)
