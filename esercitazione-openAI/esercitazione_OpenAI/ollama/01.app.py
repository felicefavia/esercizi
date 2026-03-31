import ollama

stream = ollama.chat(
    model="gemma3:4b",
     messages=[
        {
            "role": "developer", 
            "content": "Sei un traduttore professionista. Traduci testi dall'italiano all'inglese o dall'inglese all'italiano "
        },
        {
        "role": "user",
        "content": (
            "Traduci i seguenti testi:\n"
            "1. Italiano → Inglese: 'Ciao, oggi è una bella giornata'\n"
            "2. Inglese → Italiano: 'Hello, today is a beautiful day.'"
            )
        }
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)