# engine.py - Capa de IA (Motor Laya DLM)

import os
import warnings

# Silenciamos ruidos de librerías al importar
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

import laya

def inicializar_router():
    """Carga y retorna el router DLM de Laya."""
    return laya.Router(preload=True)

def analizar_con_ia(router, nombre, lista_ingredientes):
    """Realiza la predicción semántica para casos grises o ambiguos."""
    estado_actual = f"Producto: {nombre}. Ingredientes: {', '.join(lista_ingredientes)}"
    preguntas = {
        "veredicto": {
            "type": "choice",
            "instructions": "Analiza si el producto presenta algún riesgo oculto o ambigüedad para celíacos.",
            "criteria": {
                "Seguro": "El producto es totalmente apto y no presenta riesgos.",
                "Dudoso": "Contiene elementos que requieren revisión detallada por trazas."
            }
        }
    }
    resultado = router.predict(state=estado_actual, questions=preguntas)
    ans_data = resultado["answers"]["veredicto"]
    return ans_data["choice"], ans_data["probabilities"][ans_data["choice"]]
