# from "Pegue a função perguntar_gemini que está dentro de ai/gemini_client.py."

from ai.gemini_client import perguntar_gemini


def main():
    resposta = perguntar_gemini("Olá, Gemini!")
    print(resposta)



if __name__ == "__main__":
    main()