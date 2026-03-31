import ollama

input_text = input("Enter text: ")

stream = ollama.chat(
    model="gemma3:4b",
    messages=[
        {"role": "system", "content": "Sei un generatore di domande. Quando ti danno del testo, tu in base al testo fai domande inerenti all'argomento"},
        {"role": "user", "content": input_text}
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)