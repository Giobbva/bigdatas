--------------------------------------------------------------------------------
README: Dataset de Benchmark para Conciencia Ambiental de LLMs
Fecha: 28 de julio de 2025
Autor: [Tu Nombre/Equipo]
--------------------------------------------------------------------------------

OBJETIVO DEL DATASET:
Este dataset ha sido creado para evaluar la "conciencia ambiental" de los Grandes Modelos de Lenguaje (LLMs) durante sus interacciones. Busca medir la eficiencia y la necesidad real del contenido que generan, con el fin de reducir el desperdicio de recursos computacionales y la huella de carbono asociada.

ESTRUCTURA DEL DATASET (benchmark_conciencia_extendido.csv):
El archivo CSV contiene 100 prompts divididos en dos categorías principales:

1.  PROMPTS SIMPLES (IDs 1-50):
    * Preguntas directas y básicas (ej., "¿Cuál es la capital de X?").
    * Evalúan la capacidad del LLM para dar la respuesta más concisa y mínima necesaria, sin añadir información superflua.

2.  PROMPTS DE CONCIENCIA AMBIENTAL (IDs 51-100):
    * Preguntas que interrogan directamente al LLM sobre su propia eficiencia, impacto ambiental y mecanismos para reducir su huella.
    * Evalúan la comprensión del LLM sobre estos conceptos y su capacidad para articular respuestas específicas y eficientes sobre ellos.

CÓMO UTILIZAR Y EVALUAR:
1.  **Ejecuta los LLMs:** Pasa cada `prompt_text` del CSV al LLM que estés evaluando.
2.  **Guarda las Respuestas:** Almacena las respuestas generadas por el LLM para cada prompt.
3.  **Evaluación Humana:** Utiliza la "Guía Breve para la Puntuación Modificada" (que debería estar en un documento aparte, como un PDF o TXT dedicado a las instrucciones de scoring) para que evaluadores humanos califiquen cada respuesta del LLM. La puntuación debe basarse en la concisión, la relevancia y la ausencia de información innecesaria (para prompts simples) y en la profundidad/eficiencia de la comprensión (para prompts de conciencia ambiental).

IMPORTANCIA DE ESTA MÉTRICA:
Buscamos fomentar:
* Reducción de la huella de carbono de la IA.
* Uso más eficiente de los recursos computacionales.
* Promoción de interacciones más concisas y conscientes por parte de los usuarios, al "educar" a la IA para que pida especificidad.
