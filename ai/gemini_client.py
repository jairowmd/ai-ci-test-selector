import os
import requests


GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def perguntar_gemini(pergunta):
    api_key = os.getenv("GEMINI_API_KEY")

    headers = {
        "Content-Type": "application/json"
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
        params={"key": api_key},
        json=dados
    )

    print(response.status_code)
    print(response.text)


def main():
    perguntar_gemini("Olá, Gemini!")


if __name__ == "__main__":
    main()