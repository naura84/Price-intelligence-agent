import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise RuntimeError("Clé api introuvable dans le fichier env")

client = genai.Client(api_key=api_key)

#test sur la connexion avec gemini
#response = client.models.generate_content(model=model, contents="Réponds uniquement : Connexion réussie !")

#print(response.text)

#test sur la recherche web

for attempt in range(5):
    try :
        response1 = client.models.generate_content(model=model, 
                                                contents="recherche des informations récentes sur des casques bluetooth à réduction de bruit vendus en Espagne.",
                                                config = types.GenerateContentConfig(tools=[types.Tool(
                                                    google_search=types.GoogleSearch()
                                                )
                                            ]
                                        ),
        )
        break
    except Exception as e:
        if "429" in str(e):
            print("Too many request. Waiting...")
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        else :
            raise e