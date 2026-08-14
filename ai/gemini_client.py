# Responsabilidade: Conversar com o Gemini.

import os # os → permite acessar coisas do sistema operacional
import requests # requests → biblioteca que usamos para fazer requisições HTTP.


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"


def perguntar_gemini(pergunta):
    api_key = os.getenv("GEMINI_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    dados = {
        "contents": [
            {
                "parts": [
                    {
                        "text": pergunta
                    }
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        headers=headers,
        json=dados,
        timeout=60
    )

    response.raise_for_status()

    dados_resposta = response.json()

    resposta = dados_resposta["candidates"][0]["content"]["parts"][0]["text"]

    return resposta

if __name__ == "__main__":
    main()