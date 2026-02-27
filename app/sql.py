import re
import os
import json
import sqlite3
import pandas as pd
from groq import Groq
from pprint import pprint
from dotenv import load_dotenv

load_dotenv('/Users/sachinkumar/Documents/Gen AI Course/E-commerce chatbot/.env')

GROQ_MODEL = os.getenv("GROQ_MODEL")
sql_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
db_path = "/Users/sachinkumar/Documents/Gen AI Course/E-commerce chatbot/web_scrapping/db.sqlite"

def run_sql_query(query):
    if query.strip().upper().startswith('SELECT'):
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
            return df
        
sql_prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: product 

fields: 
product_link - string (hyperlink to product)	
title - string (name of the product)	
brand - string (brand of the product)	
price - integer (price of the product in Indian Rupees)	
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
total_ratings - integer (total number of ratings for the product)

</schema>
Make sure whenever you try to search for the brand name, the name can be in any case. 
So, make sure to use %LIKE% to find the brand in condition and change the brand to lower case. 
Never use "ILIKE". 
Create a single SQL query for the question provided. 
The query should have all the fields in SELECT clause (i.e. SELECT *)

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags."""

def generate_sql_query(query):

    chat_completion = sql_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sql_prompt,
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model = os.getenv("GROQ_MODEL"),
        temperature = 0.2,
        max_tokens = 1024
    )
    llm_answer = chat_completion.choices[0].message.content
    return llm_answer

def sql_chain(question):
    sql_query_tag = generate_sql_query(question)
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query_tag, re.DOTALL)
    if len(matches) == 0:
        return "Sorry LLM is not able to generate the query, try rephrasing the question"
    
    clean_sql_query = matches[0].strip()
    output_df = run_sql_query(clean_sql_query)
    if output_df is None:
        return "Sorry there was some error executing SQL query"
    
    context = output_df.to_dict(orient='records')
    final_output = comprehensive_answer(question, context)
    return final_output
    
comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
You should only provide the details from the given data. Not out of your own Specifically the urls.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in list of JSONs. Also, dont forget the delimiter.
format when asked about a product: 
Produt title, price in indian rupees, discount, and rating, and then product link. Take care that all the products are listed in list format, one line after the other. Not as a paragraph.
For example:
[
  {
    "name": "HR-060 08 Running Shoes For Women",
    "price": 1098,
    "discount": 63,
    "rating": 4.1,
    "url": "<link>"
  }
]

"""

def comprehensive_answer(question, context):

    chat_completion = sql_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": comprehension_prompt,
            },
            {
                "role": "user",
                "content": f"QUESTION: {question} CONTEXT: {context}",
            }
        ],
        model = os.getenv("GROQ_MODEL"),
        temperature = 0.2
    )
    llm_answer = chat_completion.choices[0].message.content
    return json.loads(llm_answer)

if __name__ == "__main__":
    question = "show me top 3 puma shoes with highest rating"
    answer = sql_chain(question)
    print(answer)
    print(type(answer))
    print(type(answer[0]))
    # print(answer[0]['name'])