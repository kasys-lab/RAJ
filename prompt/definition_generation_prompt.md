## Definition generation prompt for RAJ (query)

```
Given a query and documents, please generate definition sentences in Japanese for the named entity in the query with reference to the documentation. Generate the definition in one sentence according to the following example.

Example
Query:{query}
Document:{page text}
Definition Sentence:{definition sentence}

Refer to the following document and generate a definition sentence in Japanese for the named entity in the query.

Query:{query}

-BEGIN Document A-
{page text}
-END Document A-

-BEGIN Document B-
{page text}
-END Document B-

-BEGIN Document C-
{page text}
-END Document C-
```

## Definition generation prompt for RAJ (entity)

```
Given a named entity and documents, please generate a definition sentence for the named entity with reference to the documentation.
Generate the definition in one sentence according to the following example.

Example
Named Entity:{named entity}
Document:{page text}
Definition Sentence:{definition sentence}

Refer to the following three documents to generate a definition sentence for the given named entity.

Named Entity:{named entity}

-BEGIN Document A-
{page text}
-END Document A-

-BEGIN Document B-
{page text}
-END Document B-

-BEGIN Document C-
{page text}
-END Document C-
```

## Definition generation prompt for GAJ (query)

```
Given a query, please generate definition sentences for the named entity in the query. Generate the definition in one sentence according to the following example.

{example}

Generate a definition sentence for the named entity in the query.

Query:{query}
Definition sentence:
```
