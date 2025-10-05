from argparse import ArgumentParser
from ..dataset_handler.RobustHandler import RobustHandler
from ..dataset_handler.CovidHandler import CovidHandler
from ..dataset_handler.NFCorpusHandler import NFCorpusHandler


def parse():
    parser = ArgumentParser(description="generate batch file")
    parser.add_argument(
        "prompt_name",
        help="prompt name to be generated",
        choices=["generate_query_based_def", "generate_llm_query_based_def", "generate_named_entity_based_def"],
    )
    parser.add_argument(
        "dataset_name", help="the dataset name for generate batch file", choices=["robust", "covid", "nfcorpus"]
    )
    parser.add_argument("retrieved_doc_file_path", help="retrieved documents file path")
    parser.add_argument("output_file_path", help="output file path")
    args = parser.parse_args()
    return args


def generate_batch_file(args):
    MODEL_NAME = "gpt-4-0613"
    MAX_TOKEN = 8180

    if args.dataset_name == "robust":
        robust = RobustHandler()
        robust.generate_batch_file(
            args.prompt_name,
            MODEL_NAME,
            MAX_TOKEN,
            args.retrieved_doc_file_path,
            args.output_file_path,
        )

    elif args.dataset_name == "covid":
        covid = CovidHandler()
        covid.generate_batch_file(
            args.prompt_name,
            MODEL_NAME,
            MAX_TOKEN,
            args.retrieved_doc_file_path,
            args.output_file_path,
        )

    elif args.dataset_name == "nfcorpus":
        nfcorpus = NFCorpusHandler()
        nfcorpus.generate_batch_file(
            args.prompt_name,
            MODEL_NAME,
            MAX_TOKEN,
            args.retrieved_doc_file_path,
            args.output_file_path,
        )


if __name__ == "__main__":
    args = parse()
    generate_batch_file(args)
