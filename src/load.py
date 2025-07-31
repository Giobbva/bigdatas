from src.prompts import get_mongo_connection
from datetime import datetime
from langchain_core.messages import HumanMessage

def guardar_respuesta_mongo(db, coleccion, prompt_text, response_text, modelo_nombre):
    """
    Inserta una respuesta generada por un modelo en la colección correspondiente.
    """
    doc = {
        "prompt": prompt_text,
        "response": response_text,
        "model": modelo_nombre,
        "timestamp": datetime.utcnow().isoformat()
    }
    db[coleccion].insert_one(doc)
    print(f"✅ Guardado en colección '{coleccion}' para modelo {modelo_nombre}")

def evaluar_y_guardar(prompt: HumanMessage, modelo_nombre: str, modelo, db, colecciones_por_modelo: dict):
    """
    Evalúa un prompt con un modelo específico y guarda el resultado en MongoDB.
    """
    prompt_text = prompt.content
    if modelo_nombre == "Deepseek":
        response = modelo.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt_text},
            ],
            stream=False
        )
        response_text = response.choices[0].message.content
    else:
        response = modelo.invoke([prompt])
        response_text = response.content

    coleccion = colecciones_por_modelo[modelo_nombre]
    guardar_respuesta_mongo(db, coleccion, prompt_text, response_text, modelo_nombre)

def procesar_modelos(prompts, modelos, colecciones_por_modelo=None):
    """
    Evalúa todos los prompts con todos los modelos y guarda los resultados.
    """
    db = get_mongo_connection()

    if colecciones_por_modelo is None:
        colecciones_por_modelo = {
            "GPT-4o": "gpt4o_responses",
            "Claude 3 Sonnet": "claude_responses",
            "Gemini": "gemini_responses",
            "Deepseek": "deepseek_responses"
        }

    for modelo_nombre, modelo in modelos.items():
        print(f"🚀 Evaluando modelo: {modelo_nombre}")
        for prompt in prompts:
            try:
                evaluar_y_guardar(prompt, modelo_nombre, modelo, db, colecciones_por_modelo)
            except Exception as e:
                print(f"❌ Error al evaluar prompt con {modelo_nombre}: {e}")
