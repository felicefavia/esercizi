import ollama

input_text = input("Enter text: ")

stream = ollama.chat(
    model="gemma3:4b",
    messages=[
        {"role": "system", "content": "Sei un esperto di riassunti. Quando ricevi un testo, crea un riassunto di massimo 255 caratteri, manitieni le informazioni principali. Usa uno stile neutro."},
        {"role": "user", "content": input_text}
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)