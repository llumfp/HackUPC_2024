import json
import requests
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
import json
import os

openai_api_key  = 'sk-proj-L1NVHEd0yZVUGBmO7jFDT3BlbkFJY1FuNCPl1uUQD2kq51Or'

lst = [('1', '430'), ('6', '991'), ('13', '672'), ('2', '144'), ('14', '683')]

def guidance(lst:list):
        
    prompt_template = """Hey Chat! Given the list of tuples I'll provide, give me a step-by-step explanation in natural language of which section I should go to (first element of the tuple) and which product I need to pick up (second element of the tuple).

    The list is as follows:

    {lst}

    ANSWER:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["lst"])

    try:
        llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key,model_name="gpt-3.5-turbo-0613")
        initial_chain = LLMChain(llm=llm, prompt=prompt, output_key="output",verbose=True)
        result = (initial_chain.run({
                    'lst': lst,
                    }))
        return result
    except Exception as e:
        print(f"Error while calling OpenAI API {e}")

print(guidance(lst))