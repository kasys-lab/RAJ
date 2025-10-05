import os
import sys
import pandas as pd
from argparse import ArgumentParser

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.request import request_batch


def parse():
    parser = ArgumentParser(description="request azure openai api")
    parser.add_argument("model_name", help="the name of gpt version", choices=["gpt-4", "gpt-35-turbo"])
    parser.add_argument("batch_file_path", help="batch file path")
    parser.add_argument("output_file_path", help="output file path")
    args = parser.parse_args()

    return args


def main(args):
    df = pd.read_json(args.batch_file_path, orient="records", lines=True)
    content = (
        df["body"]
        .apply(lambda x: [msg.get("content") for msg in x.get("messages") if msg.get("role") == "user"])
        .explode()
    )

    request_batch(args.model_name, content, args.output_file_path)


if __name__ == "__main__":
    args = parse()
    main(args)
