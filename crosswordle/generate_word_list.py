import os
import openai
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_word_pair_list(N: int = 10):
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": f"""
                    You are an assistant helping generate content for a puzzle game. 
                    - Encase your response in three-back tick marks, ```
                    - You will generate a list of {N} two word phrases.
                    - Each row should only contain the two words.
                    - Please do not add any additional formatting for enumeration.
                """
            }
        ]
    )
    print(chat_completion.choices[0].message.content)    
    
generate_word_pair_list()