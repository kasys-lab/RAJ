from argparse import ArgumentParser
from ..dataset_handler.BaseHandler import BaseHandler


def parse():
    parser = ArgumentParser(description="evaluate relevance judgment")
    parser.add_argument("eval_dataset_file_path", help="evaluate dataset file path")
    parser.add_argument("batch_result_file_path", help="batch result file path")
    parser.add_argument("result_jsonl_file_path", help="output result jsonl file path")
    parser.add_argument("binary_result_jsonl_file_path", help="output binary result jsonl file path")
    parser.add_argument("eval_score_json_file_path", help="output summary eval score jsonl file path")
    args = parser.parse_args()
    return args


def evaluate(args):
    dataset_handler = BaseHandler()
    dataset_handler.generate_judgment_result_file(
        args.eval_dataset_file_path,
        args.batch_result_file_path,
        args.result_jsonl_file_path,
        args.binary_result_jsonl_file_path,
        args.eval_score_json_file_path,
    )


if __name__ == "__main__":
    args = parse()
    evaluate(args)
