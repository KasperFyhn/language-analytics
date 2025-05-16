import argparse

from ngrammodel import NgramModel


def main(model_name: str, data_path: str, ngram_size: int):
    model = NgramModel(model_name, ngram_size=ngram_size)
    model.train(data_path)
    model.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model_name', type=str,
                        help='Name of model under which it will be saved.')
    parser.add_argument('data_path', type=str,
                        help='Glob pattern for text files to train on.')
    parser.add_argument('-n', '--ngram-size', type=int, default=3)
    args = parser.parse_args()

    main(args.model_name, args.data_path, args.ngram_size)