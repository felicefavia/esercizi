import ollama

input_text = input("Enter text: ")

stream = ollama.chat(
    model="gemma3:4b",
     messages=[
        {"role": "developer", "content": "Sei un assistente che riesce ad estrarre informazioni come nome, età e professione. Estrai le informazioni personali ed elencale come una lista."},
        {"role": "user", "content": input_text}
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)