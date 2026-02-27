import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv('/Users/sachinkumar/Documents/Gen AI Course/E-commerce chatbot/.env')

groq_client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

def small_talk_generator(query):

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model = os.getenv("GROQ_MODEL"),
        temperature = 0.9,
        # max_tokens = 500
    )
    llm_answer = chat_completion.choices[0].message.content
    return llm_answer

if __name__ == "__main__":
    answer = small_talk_generator("Who are you?")
    print(answer)