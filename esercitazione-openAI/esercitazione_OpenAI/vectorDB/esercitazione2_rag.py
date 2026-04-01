import os 
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import OpenAI

document_dir = "ricette"

documents = []
metadatas = []
ids = []

id = 0
key = load_dotenv('../.env')

# Recupera i documenti dalla cartella resumes
for filename in os.listdir(document_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(document_dir, filename), 'r') as file:
            chuncks = file.read().replace('\n', '.').split('###')

            for chunk in chuncks:
                if not chunk.isspace() and not chunk == "":
                    documents.append(chunk)
                    metadatas.append({"source": filename})
                    ids.append(str(id))
                    id +=1

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="inserire api key",
    model_name="text-embedding-3-small"
)

# Inizializziamo chroma client
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="ricettario",
    embedding_function=openai_ef
)

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

# user_question = "Ciao, oggi ho tanta voglia di prepararmi un piatto vegetariano. Sai consigliarmi qualcosa?"

user_question = input("Enter text: ")


results = collection.query(
    query_texts=[user_question],
    n_results=1
)

context = f"CONTESTO: nome file {results['metadatas'][0][0]['source']} ecco il paragrafo piu significativo {results['documents'][0][0]}"


prompt = f"""Dato il seguente contesto {context} rispondi alla domande dell'utente {user_question}
spiegando che nel file individuato c'è la ricetta più adatta.
Argomenta la scelta utilizzando il contenuto del testo individuato nel contesto"""

client = OpenAI()

completion = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {
            "role": "developer",
            "content": "Sei un ricettario, specializzato nella ricerca di ricette inerenti alla richiesta"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(completion.choices[0].message.content)