import os
import pandas as pd
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
import warnings

warnings.filterwarnings('ignore')
load_dotenv('/Users/sachinkumar/Documents/Gen AI Course/E-commerce chatbot/.env')

BASE_DIR = Path(__file__).resolve().parent.parent
faq_path = BASE_DIR / "resources" / "faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faq = 'faqs'
ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
groq_client = Groq(api_key = st.secrets.get("GROQ_API_KEY")

def ingest_faq_data(path):
    print(f"Injestion FAQ data to chroma")
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        collection = chroma_client.get_or_create_collection(
            name = collection_name_faq,
            embedding_function = ef
        )

        df = pd.read_csv(path)
        docs = df['question'].to_list()
        metadata = [{"answer": ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(1, len(docs)+1)]

        collection.add(
            documents = docs,
            metadatas = metadata,
            ids = ids
        )
        print(f"FAQ Data successfully injested into chroma collection: {collection_name_faq}")
    else:
        print(f"Collection {collection_name_faq} already exist!")

def get_relevent_qa(query):
    collection = chroma_client.get_collection(collection_name_faq)
    result = collection.query(
        query_texts = [query],
        n_results = 2
    )
    return result

def generate_answer(query, context):
    prompt = f'''Given the question and context below, generate the answer based on the context only.
    If you dont find the answer inside the context then say I don't know
    Don't make things up.

    Question: {query}

    Context: {context}
    '''

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model = st.secrets.get("GROQ_MODEL"),
    )
    llm_answer = chat_completion.choices[0].message.content
    return llm_answer

def faq_chain(query):
    relevant_ans = get_relevent_qa(query)
    context = ''.join([r.get('answer') for r in relevant_ans.get('metadatas')[0]])
    answer = generate_answer(query, context)
    return answer


if __name__ == "__main__":
    ingest_faq_data(faq_path)
    query = "Do you offer international shipping?"
    final_ans = faq_chain(query)
    print("----------------------------------------------------------------------------")
    print("\n")
    print(f"Answer: {final_ans}")
    print("\n")
