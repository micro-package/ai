import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


model_lst = openai.Model.list()

for i in model_lst['data']:
    print(i['id'])
