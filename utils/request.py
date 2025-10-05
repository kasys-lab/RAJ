import os
import json
import tqdm
from dotenv import load_dotenv
from openai import AzureOpenAI


def request_batch(model_name, content, output_file_path):
    load_dotenv()

    result = []
    print(f"\n selected model : {model_name}\n")

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_KEY_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    print("\n batch progress\n")
    for i in tqdm.tqdm(range(len(content))):
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "",
                },
                {"role": "user", "content": content[i]},
            ],
            temperature=0,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0,
        )
        res = response.choices[0].message.content
        result.append(
            {
                "response": {
                    "status_code": 200,
                    "body": {
                        "object": "chat.completion",
                        "model": model_name,
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": res,
                                },
                            }
                        ],
                    },
                },
            }
        )

    with open(output_file_path, "w", encoding="utf-8") as f:
        for res in result:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
        print(f"\ncompleted")
