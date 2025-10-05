from argparse import ArgumentParser
from ..dataset_handler.RobustHandler import RobustHandler
from ..dataset_handler.CovidHandler import CovidHandler
from ..dataset_handler.NFCorpusHandler import NFCorpusHandler


def parse():
    parser = ArgumentParser(description="creates an eval dataset")
    parser.add_argument(
        "dataset_name", help="the dataset name for relevance judgment", choices=["robust", "covid", "nfcorpus"]
    )
    parser.add_argument("output_file_path", help="output file path")
    args = parser.parse_args()
    return args


def generate_eval_dataset(args):
    MAX_TOKEN = 3800

    if args.dataset_name == "robust":
        robust = RobustHandler()
        robust.load_dataset("disks45/nocr/trec-robust-2004")
        robust.sample_eval_data(MAX_TOKEN, 1800, 900, 900, args.output_file_path)

    elif args.dataset_name == "covid":
        covid = CovidHandler()
        covid.load_dataset("beir/trec-covid")
        covid.sample_eval_data(MAX_TOKEN, 2000, 1000, 1000, args.output_file_path)

    elif args.dataset_name == "nfcorpus":
        nfcorpus = NFCorpusHandler()
        nfcorpus.load_dataset("beir/nfcorpus/test")
        nfcorpus.sample_eval_data(MAX_TOKEN, 1000, 500, 500, args.output_file_path)


if __name__ == "__main__":
    args = parse()
    generate_eval_dataset(args)
