## Prompt for measuring document specialization level

```
Given a document, you must provide a score on an integer scale of 0 to 2 evaluating its level of expertise with the following meanings:
2 = Highly specialized: Clearly targeted at experts, contains in-depth technical analysis, jargon, and specialized discussion in a specific domain.
1 = Moderately specialized: Includes some technical terms or domain-specific knowledge but remains accessible to non-experts.
0 = Non-specialized: The content is superficial, lacks technical terms, and is aimed at a general audience.

Assume that you are writing a professional report in the domain. If you would quote or use content from this document directly:
Mark 2 if the content is highly specialized and crucial for the report.
Mark 1 if some parts are usable but not all are specialized.
Mark 0 if the document is not suitable for inclusion due to low expertise level.

Please output your answer in the following format, including both the score and a brief explanation:
{"score": score, "explanation": "Your explanation here."}

Document: {doc}
Output:
```

## Prompt for measuring query specialization level

```
Given a query, you must provide a score on an integer scale of 0 to 2 evaluating its level of expertise with the following meanings:
2 = Highly specialized: Clearly intended for experts, includes technical terminology, and reflects deep understanding of a specific domain.
1 = Moderately specialized: Contains some domain-specific language or implies familiarity with the field, but still understandable by a broader audience.
0 = Non-specialized: General in nature, lacks domain-specific terminology, and does not require expert knowledge to understand.

Assume that you are writing a professional report in the domain. If you were to assess how specialized the topic of this query is for inclusion in such a report:
Mark 2 if the topic is highly specialized and clearly appropriate for expert-level discussion.
Mark 1 if the topic is moderately specialized and shows some technical depth.
Mark 0 if the topic is too general or not suitable for a specialized report.

Please output your answer in the following format, including both the score and a brief explanation:
{{"score": score, "explanation": "Your explanation here."}}

Query: {query}
Output:
```
