## Relevance judgment prompt

```
Given a query and a document, you must provide a score on an integer scale of 0 to 2 with the following meanings:

2 = highly relevant, very helpful for this query
1 = relevant, may be partly helpful but might contain other irrelevant content
0 = not relevant, should never be shown for this query

Assume that you are writing a report on the subject of the topic. If you would use any of the information contained in the document in such a report, mark it 1.If the document is primarily about the topic, or contains vital information about the topic, mark it 2. Otherwise, mark it 0.

Query
A person has typed {query} into a search engine.

Please use following information to help evaluate relevance.
Reference information about the query:
{definition}

Result
Consider the following web page.
-BEGIN WEB PAGE CONTENT-
{page text}
-END WEB PAGE CONTENT-

Instructions
Split this problem into steps:
Consider the underlying intent of the search.
Decide on a final score(O).
Produce a JSON array of scores without providing any reasoning. Examples:
	[{"O" : 1}]

Results [
```
