import requests
from langchain.chat_models import init_chat_model # funcion para usar modelos
from langchain_core.messages import HumanMessage # este es nuestro prompt
import os # funcion de utilidades
import pandas as pd
import airflow.models import Variable
#importar el dataset y cambiar los evaluation propmpts 

def call_deepseek():
    URL = 'https://openrouter.ai/api/v1'
    api_key = Variable.get("openrouter_api_key", default_var=None)
    if not api_key:
        print("Papu papu no hay variable open router en call_deepseek papu")
        return

    connection_parameters = {
        'openai_api_base': URL,
        'openai_api_key': api_key
    }
    call_model = init_chat_model(model='deepseek/deepseek-chat-v3-0324:free', model_provider='openai', **connection_parameters)

def call_chatgpt():

def call_gemini():

#api conexion
openai_api_key = os.getenv('OPENROUTER_API_KEY')

if openai_api_key is None:
    raise ValueError("La variable de entorno 'OPENROUTER_API_KEY' no está configurada.")

my_connection = {
    'openai_api_base': 'https://openrouter.ai/api/v1',
    'openai_api_key': openai_api_key
}

modelo1 = init_chat_model(model='deepseek/deepseek-chat-v3-0324:free', model_provider='openai', **my_connection)
modelo2 = init_chat_model(model='openai/chatgpt-4o-latest', model_provider='openai', **my_connection)
modelo3 = init_chat_model(model='google/gemini-2.5-flash', model_provider='openai', **my_connection)

modelos_a_evaluar = [
    {'name': 'Modelo 1 (Deepseek V3)', 'instance': modelo1},
    {'name': 'Modelo 2 (GPT 4o)', 'instance': modelo2},
    {'name': 'Modelo 3 (Gemini 2.5)', 'instance': modelo3},
]
#aqui van a ir los data sets
evaluation_prompts = []

all_models_responses = {
    model_info['name']: [] for model_info in modelos_a_evaluar
}
def invoque_evals(model_name,model_instance):
    for prompt in evaluation_prompts:
        response = model_instance.invoke([prompt])

        dict_responses = {
                'prompt': prompt.content, 
                'response': response.content,
                'completion_tokens': response.response_metadata.get('token_usage', {}).get('completion_tokens', 'N/A')
            }
        all_models_responses[model_name].append(dict_responses)
        print(f"  - Prompt procesado para {model_name}")