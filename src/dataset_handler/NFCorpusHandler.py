import os
import sys
import tqdm
import json
import tiktoken
import ir_datasets
import pandas as pd
from .BaseHandler import BaseHandler

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from prompts.prompt_frame import (
    generate_llm_query_based_definition_prompt,
    generate_query_based_definition_prompt,
    generate_named_entity_based_definition_prompt,
    generate_relevance_judgment_prompt,
)
from prompts.prompt_parts import (
    INTRODUCTION,
    NFCORPUS_LLM_QUERY_BASED_EXAMPLE,
    OUTPUT_EXAMPLE,
    NFCORPUS_QUERY_BASED_EXAMPLE,
    NFCORPUS_NAMED_ENTITY_BASED_EXAMPLE,
    NON_ASPECT,
)


class NFCorpusHandler(BaseHandler):
    def load_dataset(self, dataset):
        self.dataset = ir_datasets.load(dataset)
        self.df_query = pd.DataFrame(self.dataset.queries_iter())
        self.df_doc = pd.DataFrame(self.dataset.docs_iter())
        self.df_qrel = pd.read_json("data/nfcorpus_qrel.jsonl", lines=True)

    def sample_eval_data(
        self,
        max_token,
        not_relevant_count,
        partial_relevant_count,
        relevant_count,
        output_file_path,
    ):
        df_merged = pd.merge(self.df_qrel, self.df_query, on="query_id", how="left")
        df_merged = pd.merge(df_merged, self.df_doc, on="doc_id", how="left")
        df_merged = df_merged.rename(
            columns={
                "text_x": "query",
                "text_y": "doc_body",
                "title": "doc_title",
            }
        )
        df_merged = df_merged.drop(columns=["iteration", "url_x", "url_y"])
        df_filtered = self.filter_eval_data(df_merged, max_token)
        df_sampled = super().sample_data(df_filtered, not_relevant_count, partial_relevant_count, relevant_count)
        self.df_sampled = df_sampled
        print(df_sampled.info)
        df_sampled.to_json(output_file_path, orient="records", lines=True)

    def filter_eval_data(self, df, max_token):
        filtered_data = []
        encoding = tiktoken.get_encoding("cl100k_base")
        print("filtering Dataset\n")
        for i in tqdm.tqdm(range(len(df))):
            doc = f"""
                    {df["doc_title"][i]}
                    {df["doc_body"][i]}
                    """
            query = df["query"][i]
            prompt = generate_relevance_judgment_prompt(
                INTRODUCTION,
                query,
                doc,
                OUTPUT_EXAMPLE,
                NON_ASPECT,
            )
            if len(encoding.encode(prompt)) < max_token:
                filtered_data.append(
                    {
                        "query_id": df["query_id"][i],
                        "doc_id": df["doc_id"][i],
                        "relevance": df["relevance"][i],
                        "query": query,
                        "doc": doc,
                    }
                )
            else:
                continue

        df_filtered = pd.DataFrame(filtered_data)

        return df_filtered

    def generate_batch_file(
        self,
        prompt_name,
        model_name,
        max_token,
        input_file_path,
        output_file_path,
    ):
        func_table = {
            "generate_query_based_def": self.generate_definition_prompt,
            "generate_named_entity_based_def": self.generate_definition_prompt,
            "generate_llm_query_based_def": self.generate_definition_prompt,
        }
        func = func_table.get(prompt_name)
        if func:
            prompts = func(prompt_name, input_file_path, max_token)
        else:
            print("Not found prompt name")
            exit()
        request_json_file = []
        print("\ncreating batch file\n")
        for i in tqdm.tqdm(range(len(prompts))):
            request_json_file.append(
                {
                    "custom_id": f"request-{i}",
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": model_name,
                        "temperature": 0,
                        "top_p": 1.0,
                        "frequency_penalty": 0.5,
                        "presence_penalty": 0,
                        "messages": [
                            {
                                "role": "system",
                                "content": "",
                            },
                            {"role": "user", "content": prompts[i]},
                        ],
                    },
                }
            )
        with open(output_file_path, "w", encoding="utf-8") as f:
            for item in request_json_file:
                json.dump(item, f, ensure_ascii=False)
                f.write("\n")
            print(f"\nbatch file size={len(request_json_file)}")

    def generate_definition_prompt(self, prompt_name, input_file_path, max_token):
        prompt_list = []
        encoding = tiktoken.get_encoding("cl100k_base")
        if prompt_name == "generate_query_based_def":
            func = generate_query_based_definition_prompt
            example = NFCORPUS_QUERY_BASED_EXAMPLE
            keyword = "query"
        elif prompt_name == "generate_named_entity_based_def":
            func = generate_named_entity_based_definition_prompt
            example = NFCORPUS_NAMED_ENTITY_BASED_EXAMPLE
            keyword = "named_entity"
        elif prompt_name == "generate_llm_query_based_def":
            func = generate_llm_query_based_definition_prompt
            example = NFCORPUS_LLM_QUERY_BASED_EXAMPLE
            keyword = "query"

        keyword_doc_paris, keywords = self.read_keyword_doc_pairs_jsonl(keyword, input_file_path)
        if func:
            print("\ngenerating prompt\n")
            for i in tqdm.tqdm(range(len(keyword_doc_paris))):
                texts = self.get_texts(keyword_doc_paris, keywords[i])
                prompt = func(keywords[i], example, texts)
                if len(encoding.encode(prompt)) > max_token:
                    print(f"Document {keywords[i]} exceeds maximum token limit")
                    exit()
                else:
                    prompt_list.append(prompt)
        else:
            print("Not found prompt name")
            exit()

        return prompt_list

    def read_keyword_doc_pairs_jsonl(self, keyword, input_file):
        keyword_doc_pair = {}
        keywords = []
        with open(input_file, "r", encoding="utf-8") as infile:
            for line in infile:
                item = json.loads(line)
                keyword_doc_pair[item[keyword]] = item["content"]
                keywords.append(item[keyword])
        return keyword_doc_pair, keywords

    def get_texts(self, query_doc_pair, word):
        res = []
        for item in query_doc_pair[word]:
            res.append(item["text"])
        return res
