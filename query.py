import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

os.environ['OPENAI_API_KEY'] = 'sk-X7j5lfY296Z8RennPYXrfpl42uyW2gV6001JQkhzt8T3BlbkFJjEFva2F-Dg2GdIGY41UEoLTLp5keuywBo5zF0eqhcA'
openai.api_key = os.environ['OPENAI_API_KEY']

PROMPT_TEMPLATE = """
Jawablah pertanyaan berdasarkan konteks berikut ini:

{context}

---


Jawablah pertanyaan berdasarkan konteks diatas: {question}
"""

def terakhir(qwery):
    query_text = qwery

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
