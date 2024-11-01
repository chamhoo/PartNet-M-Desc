
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv


# Single Query
def single_quert(sentence, model, max_tokens=1024):
    # API KEY
    load_dotenv()
    api_key = os.getenv("OPEN_AI_KEY")

    # set client
    client = OpenAI(
        api_key=api_key
    )
    
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": sentence}],
        max_tokens = max_tokens,
        temperature=0.5,
        )
    return completion.choices[0].message.content


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# Querys in a continous manner
class VLMSession:
    def __init__(self, model, max_tokens=1024, temperature=0.5):
        load_dotenv()
        self.api_key = os.getenv("OPEN_AI_KEY")
        self.client = OpenAI(
            api_key=self.api_key
        )
        self.model = model
        self.max_tokens = max_tokens
        self.history = []
        self.temperature = temperature


    def add_to_history(self, role, content):
        self.history.append({"role": role, "content": content})


    def query(self, quary_list):
        contents = []
        for content in quary_list:
            if content["type"] == "text":
                contents.append(content)
            if content["type"] == "image":
                base64_image = encode_image(content["path"])
                img_message = {
                    "type": "image_url",
                    "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"}
                }
                contents.append(img_message)
        self.add_to_history("user", contents)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        response_content = completion.choices[0].message.content
        self.add_to_history("assistant", response_content)
        return response_content

    def get_history(self):
        return self.history




# Test
if __name__ == "__main__":
    # model reference 
    # - https://platform.openai.com/docs/models
    # - https://build.nvidia.com/meta/llama3-70b
    MODEL = "gpt-4o"

    # An example on single_quert
    print(single_quert("How are you?", MODEL))

    # An example on LLMSession
    session = VLMSession(MODEL, max_tokens=1024, temperature=0.5)
    print(session.query("What about Ale?"))
    print(session.query("What about Bob?"))
    print(session.query("What about Charlie?"))
    print(session.get_history())