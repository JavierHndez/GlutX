# app.py - Backend FastAPI para GLUTENFROID (Arquitectura Híbrida)

import os
import warnings

# Silenciamos ruidos antes de importar librerías
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from rules import evaluar_determinista
from engine import inicializar_router, analizar_con_ia

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="GLUTENFROID API",
    description="Backend de detección híbrida de gluten",
    version="1.0.0"
)

# Cargamos el motor al arrancar el servidor en Render
print("Cargando motor DLM en memoria para el servidor API...")
router = inicializar_router()
print("¡Motor listo y servidor preparado!")

# Modelo de datos de entrada esperado (Pydantic)
class ProductoRequest(BaseModel):
    nombre: str
    ingredientes: List[str]

@app.post("/analizar")
def analizar_producto(producto: ProductoRequest):
    """
    Endpoint principal para analizar un producto de forma híbrida.
    """
    try:
        nombre = producto.nombre
        ingredientes = producto.ingredientes
        
        # 1. Capa Determinista Inteligente
        estado_filtro, detalle = evaluar_determinista(ingredientes)
        
        if estado_filtro == "BLOCK":
            return {
                "producto": nombre,
                "veredicto": "CON GLUTEN",
                "nivel_alerta": "ROJO",
                "metodo": f"Filtro Determinista [{detalle}]",
                "confianza": 1.0
            }
        else:
            # 2. Capa de IA (DLM) para PASS o REVIEW
            veredicto_ia, conf = analizar_con_ia(router, nombre, ingredientes)
            
            if estado_filtro == "REVIEW":
                metodo = f"Revisión de zona gris: {detalle}"
                if "trazas" in detalle.lower() or "advertencia" in detalle.lower():
                    nivel_alerta = "AMARILLO"
                    veredicto = "PRECAUCIÓN / TRAZAS"
                else:
                    nivel_alerta = "VERDE" if veredicto_ia == "Seguro" else "AMARILLO"
                    veredicto = "SEGURO (Exención técnica)" if veredicto_ia == "Seguro" else "REVISAR"
            else:
                metodo = "Motor DLM (Laya)"
                nivel_alerta = "VERDE" if veredicto_ia == "Seguro" else "AMARILLO"
                veredicto = "SEGURO" if veredicto_ia == "Seguro" else "REVISAR"
                
            return {
                "producto": nombre,
                "veredicto": veredicto,
                "nivel_alerta": nivel_alerta,
                "metodo": metodo,
                "confianza": round(float(conf), 4)
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "online", "system": "GLUTENFROID Core Active"}
