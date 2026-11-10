# app.py - Backend FastAPI optimizado y autónomo para GLUTENFROID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="GLUTENFROID API",
    description="Backend de detección rápida de gluten por reglas deterministas",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (tu web móvil)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Palabras clave y listas negras estrictas
HARD_BLACKLIST = ["trigo", "cebada", "centeno", "malta", "triticale", "espelta", "kamut"]
WARNING_KEYWORDS = ["trazas", "puede contener", "contacto", "fábrica", "trazas de"]

class ProductoRequest(BaseModel):
    nombre: str
    ingredientes: List[str]

@app.post("/analizar")
def analizar_producto(producto: ProductoRequest):
    """
    Endpoint principal de análisis ultra-rápido por reglas.
    """
    try:
        nombre = producto.nombre
        ingredientes = producto.ingredientes
        
        for ing in ingredientes:
            lower_ing = ing.lower()
            
            # 1. Comprobar advertencias de trazas (Amarillo)
            for warn in WARNING_KEYWORDS:
                if warn in lower_ing:
                    return {
                        "producto": nombre,
                        "veredicto": "PRECAUCIÓN / TRAZAS",
                        "nivel_alerta": "AMARILLO",
                        "metodo": f"Advertencia de contaminación cruzada: '{ing}'",
                        "confianza": 0.85
                    }
            
            # 2. Comprobar cereales prohibidos (Rojo o Excepción Verde)
            for cereal in HARD_BLACKLIST:
                if cereal in lower_ing:
                    # Excepciones técnicas seguras (ej. jarabe de glucosa o sin gluten certificado)
                    if "sin gluten" in lower_ing or ("jarabe de glucosa" in lower_ing and "trigo sin especificar" not in lower_ing):
                        return {
                            "producto": nombre,
                            "veredicto": "SEGURO (Exención técnica)",
                            "nivel_alerta": "VERDE",
                            "metodo": f"Contiene '{cereal}', pero cumple exención técnica apta.",
                            "confianza": 0.95
                        }
                    else:
                        return {
                            "producto": nombre,
                            "veredicto": "CON GLUTEN",
                            "nivel_alerta": "ROJO",
                            "metodo": f"Cereal prohibido directo: '{cereal}'",
                            "confianza": 1.0
                        }
        
        # Si pasa todo sin coincidencias
        return {
            "producto": nombre,
            "veredicto": "SEGURO",
            "nivel_alerta": "VERDE",
            "metodo": "Filtro Determinista (Sin alérgenos detectados)",
            "confianza": 1.0
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "online", "system": "GLUTENFROID Core Active (Fast & Pure Rules)"}
