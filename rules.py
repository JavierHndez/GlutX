# rules.py - Capa Determinista de Dos Niveles

HARD_BLACKLIST = ["trigo", "cebada", "centeno", "malta", "triticale", "espelta", "kamut"]
WARNING_KEYWORDS = ["trazas", "puede contener", "contacto", "fábrica"]

def evaluar_determinista(lista_ingredientes):
    """
    Clasifica el riesgo de los ingredientes:
    - 'BLOCK': Prohibición absoluta y directa.
    - 'REVIEW': Advertencias de trazas o derivados técnicos que requieren criterio de IA.
    - 'PASS': Sin indicios de riesgo.
    """
    for ing in lista_ingredientes:
        ing_lower = ing.lower()
        
        # 1. Detectar alertas de contaminación cruzada o trazas
        for warn in WARNING_KEYWORDS:
            if warn in ing_lower:
                return "REVIEW", f"Advertencia de trazas: '{ing}'"
                
        # 2. Detectar cereales prohibidos estrictos
        for cereal in HARD_BLACKLIST:
            if cereal in ing_lower:
                # Excepciones técnicas o normativas que la IA debe evaluar con lupa
                if "sin gluten" in ing_lower or "jarabe de glucosa" in ing_lower:
                    return "REVIEW", f"Derivado o exención en revisión: '{ing}'"
                else:
                    return "BLOCK", f"Cereal prohibido directo: '{cereal}'"
                    
    return "PASS", "Limpio"
