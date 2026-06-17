import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

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

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text