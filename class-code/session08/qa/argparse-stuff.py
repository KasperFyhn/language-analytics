import argparse


def main_function(first_argument, second_argument):
    print("First argument:", first_argument)
    print("Second argument:", second_argument)


if __name__ == "__main__":

    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Demo of various argparse argument styles'
    )

    # Positional arguments
    parser.add_argument('first_argument', help='A positional argument (required)')

    # Optional argument that requires a value
    parser.add_argument('--second-argument', type=int, default=10,
                        help='An integer argument with default value')

    # Get arguments
    args = parser.parse_args()

    main_function(args.first_argument, args.second_argument)
