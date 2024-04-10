from task_helpers import TaskHelper
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from openai import OpenAI
from langchain.docstore.document import Document
import requests
import uuid

# Dziś zadanie jest proste, ale nie łatwe — zaimportuj do swojej bazy wektorowej, spis linków z newslettera unknowNews z adresu:
# https://unknow.news/archiwum_aidevs.json
# [to mały wycinek bazy, jeśli chcesz pobrać całą bazę, to użyj pliku archiwum.json]

# Następnie wykonaj zadanie API o nazwie “search” — odpowiedz w nim na zwrócone przez API pytanie. Odpowiedź musi być adresem URL kierującym do jednego z linków unknowNews. Powodzenia!

# Note: this tasks uses qdrant database (vector db) to store vectors
# uuid4 is used to generate ids for items in qdrant

collection_name = 'ai_devs_task'
langchain_documents = []
vectors = []

# Get Task
task_helper = TaskHelper()
token = task_helper.auth("search")
task = task_helper.get_task(token, True)

# Initialize
qdrant_client = QdrantClient(host="localhost", port=6333)
openai_client = OpenAI(api_key=TaskHelper.OPENAI_API_KEY)

# Download JSON lib file and create documents
json_data = requests.get('https://unknow.news/archiwum_aidevs.json').json()
for item in json_data:
    doc = Document(
        page_content=item['info'].replace("INFO: ", "", 1),
        metadata={"title": item['title'], "url": item['url'], "date": item['date']}
    )
    langchain_documents.append(doc)

# Create embeddings (vectors + metadata)
# Knowledge base
for doc in langchain_documents:
    point = openai_client.embeddings.create(
        input=doc.page_content,
        model='text-embedding-ada-002'
    )
    vectors.append({"id": str(uuid.uuid4()), "payload": doc.metadata, "vector": point.data[0].embedding})

# Search embedding
search_embedding = openai_client.embeddings.create(
        input=task['question'],
        model='text-embedding-ada-002'
    )

# Check if collection exists
if not qdrant_client.collection_exists(collection_name):
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )
# Check if there is some indexed data (stupid approach, but still)
collection_info = qdrant_client.get_collection(collection_name=collection_name)
if not collection_info.points_count:
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                    id=vector['id'],
                    vector=vector['vector'],
                    payload=vector['payload']
            )
            for vector in vectors
        ]
    )

# Query qdrant
search_result = qdrant_client.search(
    collection_name=collection_name,
    query_vector=search_embedding.data[0].embedding,
    limit=1
)

task_helper.send_task(token, search_result[0].payload['url'])
