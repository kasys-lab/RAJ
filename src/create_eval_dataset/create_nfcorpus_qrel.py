import os
import sys
import ir_datasets
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


def generate_nfcorpus_qrel():
    dataset = ir_datasets.load("beir/nfcorpus/test")
    df_qrel = pd.DataFrame(dataset.qrels_iter())
    with open("data/nfcorpus_bm25.trec", mode="r") as f:
        lines = f.readlines()

    data = [line.split() for line in lines]
    columns = ["query_id", "Q0", "doc_id", "rank", "score", "system"]
    df = pd.DataFrame(data, columns=columns)
    df_filtered = df[["query_id", "doc_id", "rank"]].copy()
    df_filtered["rank"] = pd.to_numeric(df_filtered["rank"])
    df_filtered = df_filtered[df_filtered["rank"] <= 100]

    df_merged = pd.merge(df_qrel, df_filtered, on=["query_id", "doc_id"], how="outer")
    df_merged = df_merged.fillna(int(0))
    df_merged[["relevance", "rank"]] = df_merged[["relevance", "rank"]].astype(int)

    print(df_merged["relevance"].value_counts())
    df_merged.to_json("data/nfcorpus_qrel_test.jsonl", orient="records", lines=True)


if __name__ == "__main__":
    generate_nfcorpus_qrel()
