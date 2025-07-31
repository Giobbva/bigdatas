import os
import pandas as pd
from langchain_core.messages import HumanMessage
from pymongo import MongoClient
from airflow.models import Variable
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.getenv("CSV_PROMPTS_PATH", "/app/data/EA_Benchmark_Prompts_200.csv")

def cargar_prompts_desde_csv(path_csv=CSV_PATH):
    df = pd.read_csv(path_csv)
    if "question" not in df.columns:
        raise ValueError("El archivo CSV debe contener una columna llamada 'question'")
    return [HumanMessage(content=row["question"]) for _, row in df.iterrows()]

def get_mongo_connection():
    mongo_uri = Variable.get("mongo_uri", default_var="mongodb://root:example@mongo:27017/admin")
    client = MongoClient(mongo_uri)
    db = client["etl_processed"]
    return db

def cargar_prompts_desde_mongo(coleccion="raw_prompts", limite=None):
    db = get_mongo_connection()
    cursor = db[coleccion].find({}, {"question": 1}).limit(limite or 0)
    return [HumanMessage(content=doc["question"]) for doc in cursor if "question" in doc]