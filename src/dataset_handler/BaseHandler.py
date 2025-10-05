import re
import os
import sys
import json
import tqdm
import tiktoken
import ir_datasets
import pandas as pd
import numpy as np
import krippendorff
from collections import Counter
from sklearn.metrics import accuracy_score, cohen_kappa_score, classification_report

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from prompts.prompt_frame import (
    generate_relevance_judgment_prompt,
    generate_relevance_judgment_prompt_with_definiton,
)
from prompts.prompt_parts import (
    INTRODUCTION,
    NON_ASPECT,
    OUTPUT_EXAMPLE,
)


class BaseHandler:
    # Create evaluation dataset -------------------------------------------------------------
    def load_dataset(self, dataset):
        self.dataset = ir_datasets.load(dataset)
        self.df_query = pd.DataFrame(self.dataset.queries_iter())
        self.df_doc = pd.DataFrame(self.dataset.docs_iter())
        self.df_qrel = pd.DataFrame(self.dataset.qrels_iter())

    def sample_data(self, df, not_relevant_count, partial_relevant_count, relevant_count):
        df_sampled = pd.concat(
            [
                df[df["relevance"] == 0].sample(n=not_relevant_count, random_state=42),
                df[df["relevance"] == 1].sample(n=partial_relevant_count, random_state=42),
                df[df["relevance"] == 2].sample(n=relevant_count, random_state=42),
            ],
            ignore_index=True,
        )
        return df_sampled

    # --------------------------------------------------------------------------------------

    # Extracting queries for definition generation from the evaluation dataset -------------
    def extract_query(self, input_file_path, output_file_path):
        df = pd.read_json(input_file_path, lines=True)
        unique_queries = df["query"].unique()
        with open(output_file_path, "w", encoding="utf-8") as f:
            for query in unique_queries:
                json_line = json.dumps({"query": query}, ensure_ascii=False)
                f.write(json_line + "\n")
        print("Created unique_queries.jsonl")

    # --------------------------------------------------------------------------------------

    # Generate a batch file for OpenAI API requests ----------------------------------------
    def generate_batch_file(
        self,
        prompt_name,
        model_name,
        max_token,
        input_file_path,
        output_file_path,
    ):
        func_table = {
            "eval_non": self.generate_relevance_judgment_prompt,
            "eval_def": self.generate_relevance_judgment_prompt_with_definiton,
            "eval_doc": self.generate_relevance_judgment_prompt_with_searched_doc,
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

    # --------------------------------------------------------------------------------------

    # Generate a baseline prompt -----------------------------------------------------------
    def generate_relevance_judgment_prompt(self, prompt_name, input_file_path, max_token):
        prompt_list = []
        encoding = tiktoken.get_encoding("cl100k_base")
        df = pd.read_json(input_file_path, lines=True)
        print("\ngenerating prompt\n")
        for i in tqdm.tqdm(range(len(df))):
            doc_id = df["doc_id"][i]
            doc = df["doc"][i]
            query = df["query"][i]
            prompt = generate_relevance_judgment_prompt(INTRODUCTION, query, doc, OUTPUT_EXAMPLE, aspect=NON_ASPECT)
            if len(encoding.encode(prompt)) > max_token:
                print(f"Document {doc_id} exceeds maximum token limit.")
                exit()
            else:
                prompt_list.append(prompt)

        return prompt_list

    # --------------------------------------------------------------------------------------

    # Generate a RAJ prompt ----------------------------------------------------------------
    def generate_relevance_judgment_prompt_with_definiton(self, prompt_name, input_file_path, max_token):
        prompt_list = []
        encoding = tiktoken.get_encoding("cl100k_base")
        df = pd.read_json(input_file_path, lines=True)
        print("\ngenerating prompt\n")
        for i in tqdm.tqdm(range(len(df))):
            doc_id = df["doc_id"][i]
            doc = df["doc"][i]
            query = df["query"][i]
            definition = df["definition"][i]
            prompt = generate_relevance_judgment_prompt_with_definiton(
                INTRODUCTION, query, definition, doc, OUTPUT_EXAMPLE, aspect=NON_ASPECT
            )
            if len(encoding.encode(prompt)) > max_token:
                print(f"Document {doc_id} exceeds maximum token limit.")
                exit()
            else:
                prompt_list.append(prompt)

        return prompt_list

    # --------------------------------------------------------------------------------------

    # Generate a GAJ prompt ----------------------------------------------------------------
    def generate_relevance_judgment_prompt_with_searched_doc(self, prompt_name, input_file_path, max_token):
        prompt_list = []
        encoding = tiktoken.get_encoding("cl100k_base")
        df = pd.read_json(input_file_path, lines=True)
        print("\ngenerating prompt\n")
        for i in tqdm.tqdm(range(len(df))):
            doc_id = df["doc_id"][i]
            doc = df["doc"][i]
            query = df["query"][i]
            searched_doc = df["searched_doc"][i]
            prompt = generate_relevance_judgment_prompt_with_definiton(
                INTRODUCTION, query, searched_doc, doc, OUTPUT_EXAMPLE, aspect=NON_ASPECT
            )
            if len(encoding.encode(prompt)) > max_token:
                MAX_TOKEN = 10000
                encoding = tiktoken.get_encoding("cl100k_base")
                tokens = encoding.encode(searched_doc)
                searched_doc = encoding.decode(tokens[:MAX_TOKEN])
                prompt = generate_relevance_judgment_prompt_with_definiton(
                    INTRODUCTION, query, searched_doc, doc, OUTPUT_EXAMPLE, aspect=NON_ASPECT
                )
                if len(encoding.encode(prompt)) > max_token:
                    print(f"Document {doc_id} exceeds maximum token limit.")
                    exit()
                else:
                    prompt_list.append(prompt)
            else:
                prompt_list.append(prompt)

        return prompt_list

    # --------------------------------------------------------------------------------------

    # Evaluate -----------------------------------------------------------------------------
    def generate_judgment_result_file(
        self,
        eval_dataset_file_path,
        batch_result_file_path,
        result_jsonl_file_path,
        binary_result_jsonl_file_path,
        eval_score_json_file_path,
    ):
        result = self.bind_eval_result(eval_dataset_file_path, batch_result_file_path)
        df_result = pd.DataFrame(result)
        df_result.to_json(result_jsonl_file_path, orient="records", lines=True, force_ascii=False)
        df_binary_result = df_result.copy()
        df_binary_result["LLM_label"] = df_binary_result["LLM_label"].apply(lambda x: 2 if x in [1, 2, "1", "2"] else 0)
        df_binary_result["Ground_Truth"] = df_binary_result["Ground_Truth"].apply(
            lambda x: 2 if x in [1, 2, "1", "2"] else 0
        )
        df_binary_result.to_json(
            binary_result_jsonl_file_path,
            orient="records",
            lines=True,
            force_ascii=False,
        )
        binary_result = self.evaluate(df_binary_result)
        multi_result = self.calc_multi_value_classification(result_jsonl_file_path)
        self.save_performance_result(binary_result, multi_result, eval_score_json_file_path)

    def bind_eval_result(self, eval_dataset_file_path, batch_result_file_path):
        result = []
        df_eval = pd.read_json(
            eval_dataset_file_path,
            orient="records",
            lines=True,
        )
        df_res = pd.read_json(batch_result_file_path, orient="records", lines=True)
        for i in range(len(df_eval)):
            query_id = df_eval["query_id"][i]
            query = df_eval["query"][i]
            doc_id = df_eval["doc_id"][i]
            doc = df_eval["doc"][i]
            ground_truth = int(df_eval["relevance"][i])
            res = df_res["response"][i]
            res_value = res["body"]["choices"][0]["message"]["content"]

            o = self.parse_judgment_score(res_value)
            result.append(
                {
                    "query_id": query_id,
                    "query": query,
                    "doc_id": doc_id,
                    "doc": doc,
                    "LLM_output": res_value,
                    "LLM_label": o,
                    "Ground_Truth": ground_truth,
                }
            )
        return result

    def parse_judgment_score(self, text):
        m, t, o = 0, 0, 0
        pattern = r'{\s*"M"\s*:\s*(\d+)\s*,\s*"T"\s*:\s*(\d+)\s*,\s*"O"\s*:\s*(\d+)\s*}'
        pattern_2 = r"\d+"

        matched_list = re.findall(pattern, text)

        parsed_data = [[int(num) for num in data] for data in matched_list]

        if not parsed_data:
            matched_list = re.findall(pattern_2, text)
            if matched_list:
                m, t, o = "", "", matched_list[0]
            else:
                m, t, o = 3, 3, 3
        elif len(parsed_data) > 1:
            for i in range(len(parsed_data)):
                m += parsed_data[i][0]
                t += parsed_data[i][1]
                o += parsed_data[i][2]
            m, t, o = (
                round(t / len(parsed_data)),
                round(m / len(parsed_data)),
                round(o / len(parsed_data)),
            )
        else:
            m, t, o = parsed_data[0][0], parsed_data[0][1], parsed_data[0][2]

        return o

    def evaluate(self, df):
        y_true = df["Ground_Truth"]
        y_pred = df["LLM_label"]
        binary_kappa = cohen_kappa_score(y_true, y_pred, weights="quadratic")
        binary_krippendorff_a = self.compute_krippendorff_from_labels(y_true, y_pred)
        print(df.info)
        print("\n----- Binary Classification Result -----")
        print(classification_report(y_true, y_pred))
        print(f"kappa:{binary_kappa}")
        print(f"krippendorff_a:{binary_krippendorff_a}")
        report_dict = classification_report(y_true, y_pred, output_dict=True)
        report_dict["kappa"] = binary_kappa
        report_dict["krippendorff"] = binary_krippendorff_a

        return report_dict

    def calc_multi_value_classification(
        self,
        result_jsonl_file_path,
    ):
        df = pd.read_json(result_jsonl_file_path, orient="records", lines=True)
        print("\n----- Distribution of labels -----")
        df_highly_relevant = df[df["Ground_Truth"] == 2]
        highly_relevant_counts = Counter(df_highly_relevant["LLM_label"])
        df_partial_relevant = df[df["Ground_Truth"] == 1]
        partial_relevant_counts = Counter(df_partial_relevant["LLM_label"])
        df_irrelevant = df[df["Ground_Truth"] == 0]
        irrelevant_counts = Counter(df_irrelevant["LLM_label"])
        print(f"2:{highly_relevant_counts}")
        print(f"1:{partial_relevant_counts}")
        print(f"0:{irrelevant_counts}")

        df_result = df[["LLM_label", "Ground_Truth"]].copy()
        df_result["Ground_Truth"] = df_result["Ground_Truth"].apply(
            lambda x: (int(2) if x == 2 else (int(1) if x == 1 else 0))
        )
        y_true = df_result["Ground_Truth"]
        y_pred = df_result["LLM_label"]
        kappa_3_scale = cohen_kappa_score(y_true, y_pred, weights="quadratic")
        krippendorff_a = self.compute_krippendorff_from_labels(y_true, y_pred)
        print("\n----- Multi-Value Classification Result -----")
        print(classification_report(y_true, y_pred))
        print(f"kppa_3_scale:{kappa_3_scale}")
        print(f"krippendorff_a:{krippendorff_a}")
        report_dict = classification_report(y_true, y_pred, output_dict=True)
        report_dict["kappa"] = kappa_3_scale
        report_dict["krippendorff"] = krippendorff_a
        report_dict["2_predicted_label"] = highly_relevant_counts
        report_dict["1_predicted_label"] = partial_relevant_counts
        report_dict["0_predicted_label"] = irrelevant_counts

        return report_dict

    def compute_krippendorff_from_labels(self, y_true, y_pred, level="ordinal"):
        assert len(y_true) == len(y_pred), "y_true と y_pred の長さが一致していません"
        data = np.vstack([np.array(y_true), np.array(y_pred)])
        return krippendorff.alpha(reliability_data=data, level_of_measurement=level)

    def save_performance_result(self, binary_result, multi_resutl, eval_score_json_file_path):
        report_dict = {}
        report_dict["binary_result"] = binary_result
        report_dict["multi_result"] = multi_resutl
        with open(eval_score_json_file_path, "w") as f:
            json.dump(report_dict, f, indent=4)

    # --------------------------------------------------------------------------------------
