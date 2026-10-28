import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise RuntimeError("Clé api introuvable dans le fichier env")

client = genai.Client(api_key=api_key)

def generate_report(analysis):
    """
    Utilise un LLM pour générer un rapport
    en langage naturel, actionnable pour Diana.
    """
    
    # Préparation du contexte pour le LLM
    analysis_summary = json.dumps(analysis, ensure_ascii=False, indent=2)
    
    prompt = f"""Tu es un analyste IA spécialisé en e-commerce pour Pixmania.

Voici l'analyse comparative des prix de notre catalogue 
vs les concurrents (Amazon, Fnac, Darty, LDLC) :

{analysis_summary}

Génère un rapport business concis et actionnable pour 
Diana, notre Responsable IA. Le rapport doit inclure :

1. **RÉSUMÉ EXÉCUTIF** (2-3 phrases max)
2. **ALERTES URGENTES** (produits à repriser immédiatement)
3. **POINTS DE VIGILANCE** (produits à surveiller)
4. **OPPORTUNITÉS** (où Pixmania est compétitif)
5. **RECOMMANDATIONS** (3 actions concrètes prioritaires)

Ton style : professionnel mais direct. 
Chaque recommandation doit être actionnable en 24-48h.
Utilise des chiffres précis. Sois synthétique."""

    message = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(google_search=types.GoogleSearch()),
            ]
        ),
    )

    return message.text