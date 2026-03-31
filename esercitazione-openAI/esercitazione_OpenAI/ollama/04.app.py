import ollama

input_text = input("Enter text: ")

stream = ollama.chat(
    model="gemma3:4b",
    messages=[
        {"role": "system", "content": "Sei un esperto di elaborazione di dati. Quando ricevi un set di dati strutturati come un dizionario di python trasformalo in una descrizione testuale completa. Mantieni uno stile naturale fluido e comprensibile"},
        {"role": "user", "content": input_text}
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)