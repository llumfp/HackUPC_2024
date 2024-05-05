import json
import requests
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import json
import os
from planner import *

load_dotenv()
openai_api_key  = os.getenv('OPENAI_API_KEY')


def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo-0613"):
        
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + openai_api_key,
        }
        json_data = {"model": model, "messages": messages, "temperature": 0, "seed": 1234}


        print(f"-------------messages: {messages}")

        if tools is not None:
            json_data.update({"tools": tools})
        if tool_choice is not None:
            json_data.update({"tool_choice": tool_choice})

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            )
            print(f"response: {response}")
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e

    except Exception as e:    
        print(f"Error in chat_completion_request: {e}")


def chatbot_assistant(query,tools_accessible):


    messages = []

    messages.append({"role": "system",
        "content": f"""I am an assistance to manage your list of products to give you the right quantities. 
        I will find the products in my stock and I will say to you if I have them. I will be giving to you a number with the id. So you will need to catch the id. And only the id.
    """})


    messages.append({"role": "user", "content": query})

    chat_response = chat_completion_request(
            messages,tools=tools_accessible, model="gpt-3.5-turbo-0613"
        )
    # try:
    print(chat_response.json())
    message = chat_response.json()["choices"][0]

    if message['finish_reason'] == 'tool_calls':

        formatted_text = ""
        cont = 0
        for function in message['message']['tool_calls']:

            # Extracting the function name and arguments
            function_name = function['function']['name']
            function_arguments_str = function['function']['arguments']

            # Converting the string representation of arguments to a dictionary
            function_arguments = json.loads(function_arguments_str)

            # Using reflection to call the function by its name
            if function_name in globals():
                
                
                print(f"\n----------function called: {function_name} with arguments: {function_arguments}")
                try:
                    result = globals()[function_name](**function_arguments)

                    # prompt_template = """You are a helpful, creative, clever, friendly and professional assistant.
                    # You received the following query from the user and you executed some functions to execute:
                    # Query: {query}
                    # --END OF THE QUERY

                    # Now you've been analyzing and investigating, and came up with this result:
                    # Result: {result}

                    # What i need from you know is the following output:
                    # - Make sure the initial query from the customer is answered in english
                    # - Don't miss any detail
                    # - Answer in English always.
                    # - Don't invent any fact or add any unnecessary fact or information
                    # - Be nice and polite and offer more help, give a hint on how you can help the user
                    # - Be very short, just give the information which you have recieved. Do not add any kind of waiting for feedback sentence
                    # - Avoid any kind of message saying, for example: "If you need anything else, I am here to assist."
                    # ANSWER:"""
                    
                    prompt_template = """Hey Chat! Pass me a more human language, as someone was saying that, the following message in English. Do not say in the output anything else than the response. Be kind, as a personal assistant. Do not make lists or any kind of bullet points. Speak as human. Make sure the reply is brief and says the following information:
                    {result}
                    ANSWER:"""
                    prompt = PromptTemplate(template=prompt_template, input_variables=["result"])

                    
                    try:
                        llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key,model_name="gpt-3.5-turbo-0613")
                        initial_chain = LLMChain(llm=llm, prompt=prompt, output_key="output",verbose=True)
                        polished_result = (initial_chain.run({
                                    'result': result,
                                    }))
                    except Exception as e:
                        print(f"Error while calling OpenAI API {e}")
                    
                    polished_result = result
                except Exception as e:
                    print(f"Error while calling function {function_name} with error {e}")
                print(f"\n----------Result: {polished_result}")
            
                if(len(message['message']['tool_calls'])==1):
                    formatted_text += polished_result
                else:
                    specific_instructions = function_arguments['specific_instructions']
                    if(cont==0):
                        formatted_text += f"{specific_instructions}"
                        formatted_text += "\n"
                        formatted_text += f"\n{polished_result}"
                    else:
                        formatted_text += "\n\n"
                        formatted_text += f"────────────────────────────────────────────────"
                        formatted_text += f"\n{specific_instructions}"
                        formatted_text += "\n"
                        formatted_text += f"\n{polished_result}"

                    cont += 1

            else:
                print(f"Function '{function_name}' not found")
        
        if("\n" in formatted_text):
            formatted_text = formatted_text.replace("\n", "\n")  # Aquí podem veure quin es el format de enter que reb alexa
        else:
            formatted_text = formatted_text


        return formatted_text

    else:
        print(message['message']['content'])
        formatted_text = message['message']['content'].replace("\n", "<br>")
        return formatted_text
        
    # except Exception as e:
    #     print(f"Error in function calling: {e}")
    #     message =chat_response
    #     formatted_text = message.replace("\n", "<br>")
    #     return formatted_text


def save_json(dicc,file='product_list.json'):
    with open(file,'w') as f:
        f.write(json.dumps(dicc))

def read_json(file='product_list.json'):
    with open(file,'r') as f:
        data = json.load(f)
    return data

tool_add = {
    "type": "function",
    "function": {
        "name": "add_item",
        "description": "This function is designed to detect that the user wants to add new items to the list of products (defined by identificators)",
        "parameters": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "items": {
                        "type": "string"  # Aquí se especifica que cada elemento en el array debe ser un string
                    },
                    "description": "This parameter captures all the items the client wants to add.",
                },
                "quantities": {
                    "type": "array",
                    "items": {
                        "type": "integer"  # Aquí se especifica que cada elemento en el array debe ser un entero
                    },
                    "description": "This parameter captures the quantity of all the items the client wants to add. It should have the same order as products parameter",
                },
            },
            "required": ["products", "quantities"],
        },
    }
}
tool_modify = {}
tool_delete = {}

tool_planning = {
    "type": "function",
    "function": {
        "name": "planning_function",
        "description": "This function is used when the user want to plan a path",
        "parameters": {
            "type": "object",
            "properties": {
                "optimize": {
                    "type": "boolean",
                    "description": "This parameter captures wether the client wants to optimize or not.",
                },
            },
            "required": [],
        },
    }
}


# tools = [tool_add, tool_modify, tool_delete, tool_planning]
tools = [tool_add,tool_planning]

# Tindrem 2 diccionaris:
# 1. Stock: key = product, value = stock
# 2. Quantities: key = product, value = quantity

def find_stock(stock:dict,product:str) -> int:
    if (st := stock.get(product,None)) == None:
        return None
    else:
        return (product,int(st))

def extract_numbers(texto):
    numeros = ''.join(filter(str.isdigit, texto))
    return int(numeros)

def add_item(products,quantities):

    df = pd.read_csv('./github_repo/data_final.csv')
    stock = df.set_index('id')['cantidad'].to_dict()
    
    try:
        fquantities = read_json()
    except:
        fquantities:dict = {}

    answer = "This items have been added to the list:"
    nonavailable = []
    for p, q in zip(products, quantities):
        p = extract_numbers(p)
        p,st = find_stock(product=p, stock=stock)
        p = int(p)
        if st >= q:
            df.loc[df['id'] == p, 'cantidad'] -= q
            
            if str(p) in fquantities.keys():
                fquantities[p] += q
            else:
                fquantities[p] = q
        else:
            nonavailable.append((p,st,q))

    save_json(fquantities)

    df.to_csv('./github_repo/data_final.csv',index=False)
    
    for k,v in fquantities.items():
        answer += f'\n Product: {k}, Quantity: {v}'
    
    less_stock = False
    if nonavailable != []: answer += '\n\nWe have detected the following issues:'
    for p,st,q in nonavailable:
        if st == 0:
            answer += f"\nFor product {p}, we don't have any stock at this time."
        else:
            less_stock = True
            answer += f'\nFor product {p}, you have ordered {q} units, but we only have {st} units in stock. '
    if less_stock:
        answer += 'We are not adding the products where the stock is not enough. Specify if you want to add less quantity of them.'
    print(answer)
    return answer

def modify_quantity(product, quantity):
    pass

def delete_item(product):
    pass

def planning():
    
    pass
