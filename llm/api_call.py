from typing import List
from config import OPENAI_KEY
from openai import OpenAI


class GPT:
    def __init__(self):

        self.api_key = OPENAI_KEY
        self.model = OpenAI(api_key=self.api_key)

    def text_completion(self, user_prompt: str = "", system_prompt:str = "", tools: List = [], max_tokens: int = 500) -> str:
        """
        Get the text completion from the GPT model

        @param prompt: The prompt to be used for the completion
        @param max_tokens: The maximum number of tokens to generate
        
        ## Returns
        str: The completion text

        """
        chat_completion = self.model.chat.completions.create(
            
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="gpt-4o",
        modalities=["text"],
        )
        response_message = chat_completion.choices[0].message.content
        return response_message