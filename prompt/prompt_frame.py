import tiktoken


def generate_relevance_judgment_prompt(introduction, query, doc, output_example, aspect, context="", multiple=""):
    prompt = f"""
                {introduction} 
                
                Query 
                A person has typed [{query}] into a search engine. 
                {context}

                Please use following information to help evaluate relevance.
                Reference information about the query:null
                
                Result 
                Consider the following web page. 
                ーBEGIN WEB PAGE CONTENTー 
                {doc} 
                ーEND WEB PAGE CONTENTー 
                
                Instructions 
                Split this problem into steps: 
                Consider the underlying intent of the search. 

                {aspect}

                {multiple}
                
                Produce a JSON array of scores without providing any reasoning. Examples:{output_example}
                """
    return prompt


def generate_relevance_judgment_prompt_with_definiton(
    introduction,
    query,
    definiton,
    doc,
    output_example,
    context="",
    aspect="",
    multiple="",
):
    prompt = f"""
                {introduction} 
                
                Query 
                A person has typed [{query}] into a search engine. 
                {context}
                
                Please use following information to help evaluate relevance.
                Reference information about the query:{definiton}

                Result 
                Consider the following web page. 
                ーBEGIN WEB PAGE CONTENTー 
                {doc} 
                ーEND WEB PAGE CONTENTー 
                
                Instructions 
                Split this problem into steps: 
                Consider the underlying intent of the search. 

                {aspect}

                {multiple}
                
                Produce a JSON array of scores without providing any reasoning. Examples:{output_example}
                """
    return prompt


def generate_query_based_definition_prompt(query, example, documents):
    prompt = f"""
                Given a query and documents, please generate definition sentences for the named entity in the query with reference to the documentation. 
                Generate the definition in one sentence according to the following example.

                {example}

                Refer to the following three documents and generate a definition sentence for the named entity in the query.
                
                Query:{query}
                
                ーBEGIN Document Aー 
                {get_document(documents, 0)} 
                ーEND Document Aー 

                ーBEGIN Document Bー 
                {get_document(documents, 1)} 
                ーEND Document Bー

                ーBEGIN Document Cー 
                {get_document(documents, 2)} 
                ーEND Document Cー
                """
    return prompt


def generate_llm_query_based_definition_prompt(query, example, texts):
    prompt = f"""
                Given a query, please generate definition sentences for the named entity in the query. 
                Generate the definition in one sentence according to the following example.

                {example}

                Generate a definition sentence for the named entity in the query.

                Query:{query}
                Definition sentence:
                """

    return prompt


def generate_named_entity_based_definition_prompt(named_entity, example, documents):
    prompt = f"""
                Given a named entity and documents, please generate a definition sentence for the named entity with reference to the documentation. 
                Generate the definition in one sentence according to the following example.

                {example}

                Refer to the following three documents to generate a definition sentence for the given named entity.

                Named Entity:{named_entity}
                
                ーBEGIN Document Aー 
                {get_document(documents, 0)} 
                ーEND Document Aー 

                ーBEGIN Document Bー 
                {get_document(documents, 1)} 
                ーEND Document Bー

                ーBEGIN Document Cー 
                {get_document(documents, 2)} 
                ーEND Document Cー
                """
    return prompt


def get_document(lst, index, default=None):
    MAX_TOKEN = 2500
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(lst[index])

        if len(tokens) <= MAX_TOKEN:
            return lst[index]
        else:
            return encoding.decode(tokens[:MAX_TOKEN])
    except IndexError:
        return default


def generate_measure_expertise_of_doc_prompt(doc):
    prompt = f"""
            Given a document, you must provide a score on an integer scale of 0 to 2 evaluating its level of expertise with the following meanings:
            2 = Highly specialized: Clearly targeted at experts, contains in-depth technical analysis, jargon, and specialized discussion in a specific domain.
            1 = Moderately specialized: Includes some technical terms or domain-specific knowledge but remains accessible to non-experts.
            0 = Non-specialized: The content is superficial, lacks technical terms, and is aimed at a general audience.

            Assume that you are writing a professional report in the domain. If you would quote or use content from this document directly:
            Mark 2 if the content is highly specialized and crucial for the report.
            Mark 1 if some parts are usable but not all are specialized.
            Mark 0 if the document is not suitable for inclusion due to low expertise level.

            Please output your answer in the following format, including both the score and a brief explanation:
            {{"score": score, "explanation": "Your explanation here."}}

            Document: {doc}
            Output:
        """
    return prompt


def generate_measure_expertise_of_query_prompt(query):
    prompt = f"""
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
        """
    return prompt
