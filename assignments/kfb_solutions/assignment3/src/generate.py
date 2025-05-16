import argparse

from ngrammodel import NgramModel


def main(model_name: str, seed: str | None, tokens: int, top_k: int | None):
    model = NgramModel.load(model_name)
    if seed is not None:
        seed = tuple(seed.split())
    model.generate(seed=seed, tokens=tokens, top_k=top_k)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_name", type=str, help="The name of the model to generate with.")
    parser.add_argument('-s', '--seed', type=str, default=None, help="The seed for the text generator.")
    parser.add_argument('-t', '--tokens', type=int, default=25, help="The number of tokens to generate.")
    parser.add_argument('-k', '--top-k', type=int, default=None, help="Top-k sampling.")
    args = parser.parse_args()

    main(args.model_name, args.seed, args.tokens, args.top_k)