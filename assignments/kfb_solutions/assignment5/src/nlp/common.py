import argparse
import os


def nlp_script_args(ensure_output_dir: bool = True):
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str,
                        help="Path to the scraped JSON data files.")
    parser.add_argument("--output_path", "-o", type=str, default="output/",
                        help="Path to the directory for the CSV file.")
    args = parser.parse_args()

    # ensure output path exists
    if ensure_output_dir and not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    return args.data_path, args.output_path