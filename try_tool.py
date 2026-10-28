import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from src.loader import load_catalog
from src.tools import PriceTools

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Clé api introuvable dans le fichier env")


client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash-lite"
user_prompt = "Quels produits Pixmania doit-on repricer en urgence ?"

tool_declaration = types.FunctionDeclaration(
    name="list_at_risk_products",
    description=(
        "Liste les produits dont le prix Pixmania est plus élevé que celui du "
        "concurrent le moins cher. Renvoie la priorité, l'écart en %, le niveau "
        "de stock et si Pixmania peut s'aligner sans passer sous la marge minimale."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "min_priority": types.Schema(
                type=types.Type.STRING,
                enum=["MEDIUM", "HIGH"],
                description="HIGH pour les urgences seulement ; MEDIUM pour les urgences et les produits à surveiller.",
            )
        },
    ),
)
config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[tool_declaration])]
)

response = client.models.generate_content(
    model=MODEL,
    contents=user_prompt,
    config=config,
)

if response.function_calls:
    if not response.candidates or not response.candidates[0].content:
        raise RuntimeError("Gemini a renvoyé un appel d'outil sans contenu de réponse.")
    model_content = response.candidates[0].content

    price_tools = PriceTools(load_catalog())
    tool_functions = {
        "list_at_risk_products": price_tools.list_at_risk_products,
    }
    function_responses = []

    for function_call in response.function_calls:
        function_name = function_call.name
        if function_name not in tool_functions:
            raise ValueError(f"Gemini a demandé un outil inconnu : {function_name}")

        arguments = function_call.args or {}
        print(f"\nGemini demande l'outil {function_name} avec {arguments}")
        result = tool_functions[function_name](**arguments)
        print("Résultat de l'outil :", json.dumps(result, ensure_ascii=False, indent=2))
        function_responses.append(
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        )

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            user_prompt,
            model_content,
            types.Content(
                role="user",
                parts=function_responses,
            ),
        ],
        config=config,
    )

print("\nRéponse de Gemini :", response.text)