import argparse
import os.path

from queryexpansion import QueryExpander
from search import SearchIndex


def main(input_file, query, artist):
    index = SearchIndex(input_file)
    expander = QueryExpander()
    expanded_query = expander.expand(query)
    print(index.search(expanded_query, artist=artist))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-q', '--query', required=True, help='Query word')
    arg_parser.add_argument('-a', '--artist', required=True, help='Artist name')
    arg_parser.add_argument('-i', '--input_file', help='Input file',
                            default=os.path.dirname(__file__) +
                                    '/../data/Spotify Million Song Dataset_exported.csv')

    args = arg_parser.parse_args()
    main(args.input_file, args.query, args.artist)
