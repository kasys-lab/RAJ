from argparse import ArgumentParser
from ..dataset_handler.BaseHandler import BaseHandler


def parse():
    parser = ArgumentParser(description="generate batch file")
    parser.add_argument("prompt_name", help="prompt name to be generated", choices=["eval_non", "eval_def", "eval_doc"])
    parser.add_argument("model_name", help="model name", choices=["gpt-4-0613", "gpt-35-turbo-0613"])
    parser.add_argument("target_prompt_file_path", help="target prompt file path")
    parser.add_argument("output_file_path", help="output file path")
    args = parser.parse_args()
    return args


def generate_batch_file(args):
    MAX_TOKEN = 16000

    dataset_handler = BaseHandler()
    dataset_handler.generate_batch_file(
        args.prompt_name,
        args.model_name,
        MAX_TOKEN,
        args.target_prompt_file_path,
        args.output_file_path,
    )


if __name__ == "__main__":
    args = parse()
    generate_batch_file(args)
