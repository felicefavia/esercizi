import os 
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import OpenAI

document_dir = "resumes"

documents = []
metadatas = []
ids = []

id = 0
load_dotenv('../.env')

key_env = os.getenv("OPENAI_API_KEY")

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


# Funzione di embedding
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=key_env,
    model_name="text-embedding-3-small"
)

# Inizializzo il chroma client
chroma_client = chromadb.Client()

# Creo la collections chromaclient
collection = chroma_client.get_or_create_collection(
    name="CVs",
    embedding_function=openai_ef
)

# Aggiunge i documenti alla collection 
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids = ids
)

user_question = "Ho comprato un nuovo mobile, ma non so montarlo. Mi serve qualcuno specializzato in falegnameria che mi sappia montare il mio mobile."

results = collection.query(
    query_texts=[user_question],
    n_results=1
)

# Stampa il risultato richiesto dalla user question
# print(results)

context = f"CONTESTO: nome file {results['metadatas'][0][0]['source']} ecco il paragrafo piu significativo {results['documents'][0][0]}"

prompt = f"""Dato il seguente contesto {context} rispondi alla domande dell'utente {user_question}
spiegando che nel file individuato c'è il profilo più adatto.
Argomenta la scelta utilizzando il contenuto del testo individuato nel contesto"""

client = OpenAI()

completion = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {
            "role": "developer",
            "content": "Sei un assistente HR, specializzato nella ricerca di profili professionali"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(completion.choices[0].message.content)